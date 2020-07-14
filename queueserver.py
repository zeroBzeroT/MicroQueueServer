"""
anarchy queue server for 1.12.2 and 1.14.2 (maybe others)
includes
- join game
- freezed player position in the end
- tab
- basic chat
by bierdosenhalter
"""

from twisted.internet import reactor
from quarry.net.server import ServerFactory, ServerProtocol
from quarry.types.uuid import UUID

class Queue(ServerProtocol):
    def player_joined(self):
        # Call super. This switches us to "play" mode, marks the player as
        #   in-game, and does some logging.
        ServerProtocol.player_joined(self)

        # 1.13.2
        if self.protocol_version <= 404:
            self.send_packet("join_game",
                self.buff_type.pack("iBiBB",
                    0,                              # entity id
                    3,                              # game mode
                    1,                              # dimension
                    3,                              # difficulty
                    0),                             # Max Players	
                self.buff_type.pack_string("flat"), # level type
                self.buff_type.pack("?", False))    # reduced debug info
        else:
        # Send "Join Game" packet
            self.send_packet("join_game",
                self.buff_type.pack("iBiB",
                    0,                              # entity id
                    3,                              # game mode
                    1,                              # dimension
                    0),                             # max players
                self.buff_type.pack_string("flat"), # level type
                self.buff_type.pack_varint(1),      # view distance
                self.buff_type.pack("?", False))    # reduced debug info
   
        # Send "Player Position and Look" packet
        self.send_packet("player_position_and_look",
            self.buff_type.pack("dddff?",
                2147483647,                # x
                1337,                      # y
                2147483647,                # z
                0,                         # yaw
                0,                         # pitch
                0b00000),                  # flags
            self.buff_type.pack_varint(0)) # teleport id

        # Send "Player List Header And Footer" packet
        self.send_packet("player_list_header_footer",
            self.buff_type.pack_string("{\"translate\":\"\n \u00a7c\u00a7l0b\u00a79\u00a7l0t\u00a7a\u00a7l.org\u00a7r \n\"}"), # Header
            self.buff_type.pack_string("{\"translate\":\"\n \u00a78status \u00a7f\u00a7loffline or full \n\"}")) # Footer

        # Send "Player List Item" packet from other players
        for player in self.factory.players:
            if player.uuid != self.uuid:
                self.send_packet("player_list_item",
                    self.buff_type.pack_varint(0),                  # Action - 0: add player - VarInt
                    self.buff_type.pack_varint(1),                  # Number Of Players - VarInt
                    self.buff_type.pack_uuid(player.uuid),          # UUID
                    self.buff_type.pack_string(player.display_name),# Name - String(16)
                    self.buff_type.pack_varint(1),                  # Number Of Properties - VarInt
                    self.buff_type.pack_string("textures"),         # String (32767)
                    self.buff_type.pack_string("eyJ0aW1lc3RhbXAiOjE0NDc4NzE3MjA3OTksInByb2ZpbGVJZCI6IjA2OWE3OWY0NDRlOTQ3MjZhNWJlZmNhOTBlMzhhYWY1IiwicHJvZmlsZU5hbWUiOiJOb3RjaCIsInNpZ25hdHVyZVJlcXVpcmVkIjp0cnVlLCJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvYTExNmU2OWE4NDVlMjI3ZjdjYTFmZGRlOGMzNTdjOGM4MjFlYmQ0YmE2MTkzODJlYTRhMWY4N2Q0YWU5NCJ9LCJDQVBFIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvM2Y2ODhlMGU2OTliM2Q5ZmU0NDhiNWJiNTBhM2EyODhmOWM1ODk3NjJiM2RhZTgzMDg4NDIxMjJkY2I4MSJ9fX0="), # String (32767)
                    self.buff_type.pack("?", True),                 # Boolean
                    self.buff_type.pack_string("pLVD+OppAxCVc+1U/TSplke7bU5O+MvEz5q+ZHpsws4PoqPApFGRkRKmbMdLzvWy/ZtbtICx6nHWaHYlwVw5OP4xlKZnVTcTGA6cKdqfoGnOmxsUpq36NxuXU4wz17MYw3b+H/kQcLC8dTHGkTn/wgtHFqhZG+gL1v85FHJe/fXYT//rYuHXbvOF1ksCZRhncqUG47+oGb0+OPV4Hf5d0ZM41ON3Kzu5g0D+bYbB9uuX5MEdnHGUPLNEvhNiiXF1fJGQl1prGKgiS54MrbfSKQ9yGK1bK89avXNvlwB8u6kK99XRz4ix6HduPb4KJEm0OVWLtURw5KJfyXmxvIwmhwjX+NEoEaN/VhE9/yOZvsi+YC282GIqFafcKHj7ZbpGQP8F4mnC1GNPEumbo0WBCe8RYeaM2TFG7X5LSsyj/8k0aLbgrIP+nidKye7QaavsyZAxedcnAvnFjCGgRIQUVmO6wkBCSmJ8iHv4pCJn5B7TUCADFZaxoiGIHXSN+741Cqdev7S+QPmiubs66ESp68s926/2txFAVzH2VHYLaJ3G1dJKQUXSR4kM/246zSLYdFruPz4aTRPuPrRqcSDPoczuH+Qhp1f/1ONVYtn2+NufE9TzrxH0ZUMJ9pjQnV4aOqFj7OxZf5wjng5HHKPSK1fbbekNnV/p6h5k7kyHKuo="), # Optional String (32767)
                    self.buff_type.pack_varint(1),                  # Gamemode - VarInt
                    self.buff_type.pack_varint(42),                 # Ping - VarInt
                    self.buff_type.pack("?", True),                 # Has Display Name - Bool
                    self.buff_type.pack_chat(player.display_name))  # Display Name - Chat

        # Send "Player List Item" packet to other players
        for player in self.factory.players:
            player.send_packet("player_list_item",
                player.buff_type.pack_varint(0),                  # Action - 0: add player - VarInt
                player.buff_type.pack_varint(1),                  # Number Of Players - VarInt
                player.buff_type.pack_uuid(self.uuid),            # UUID
                player.buff_type.pack_string(self.display_name),  # Name - String(16)
                player.buff_type.pack_varint(1),                  # Number Of Properties - VarInt
                player.buff_type.pack_string("textures"),         # String (32767)
                player.buff_type.pack_string("eyJ0aW1lc3RhbXAiOjE0NDc4NzE3MjA3OTksInByb2ZpbGVJZCI6IjA2OWE3OWY0NDRlOTQ3MjZhNWJlZmNhOTBlMzhhYWY1IiwicHJvZmlsZU5hbWUiOiJOb3RjaCIsInNpZ25hdHVyZVJlcXVpcmVkIjp0cnVlLCJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvYTExNmU2OWE4NDVlMjI3ZjdjYTFmZGRlOGMzNTdjOGM4MjFlYmQ0YmE2MTkzODJlYTRhMWY4N2Q0YWU5NCJ9LCJDQVBFIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvM2Y2ODhlMGU2OTliM2Q5ZmU0NDhiNWJiNTBhM2EyODhmOWM1ODk3NjJiM2RhZTgzMDg4NDIxMjJkY2I4MSJ9fX0="), # String (32767)
                player.buff_type.pack("?", True),                # Boolean
                player.buff_type.pack_string("pLVD+OppAxCVc+1U/TSplke7bU5O+MvEz5q+ZHpsws4PoqPApFGRkRKmbMdLzvWy/ZtbtICx6nHWaHYlwVw5OP4xlKZnVTcTGA6cKdqfoGnOmxsUpq36NxuXU4wz17MYw3b+H/kQcLC8dTHGkTn/wgtHFqhZG+gL1v85FHJe/fXYT//rYuHXbvOF1ksCZRhncqUG47+oGb0+OPV4Hf5d0ZM41ON3Kzu5g0D+bYbB9uuX5MEdnHGUPLNEvhNiiXF1fJGQl1prGKgiS54MrbfSKQ9yGK1bK89avXNvlwB8u6kK99XRz4ix6HduPb4KJEm0OVWLtURw5KJfyXmxvIwmhwjX+NEoEaN/VhE9/yOZvsi+YC282GIqFafcKHj7ZbpGQP8F4mnC1GNPEumbo0WBCe8RYeaM2TFG7X5LSsyj/8k0aLbgrIP+nidKye7QaavsyZAxedcnAvnFjCGgRIQUVmO6wkBCSmJ8iHv4pCJn5B7TUCADFZaxoiGIHXSN+741Cqdev7S+QPmiubs66ESp68s926/2txFAVzH2VHYLaJ3G1dJKQUXSR4kM/246zSLYdFruPz4aTRPuPrRqcSDPoczuH+Qhp1f/1ONVYtn2+NufE9TzrxH0ZUMJ9pjQnV4aOqFj7OxZf5wjng5HHKPSK1fbbekNnV/p6h5k7kyHKuo="), # Optional String (32767)
                player.buff_type.pack_varint(1),                  # Gamemode - VarInt
                player.buff_type.pack_varint(42),                 # Ping - VarInt
                player.buff_type.pack("?", True),                 # Has Display Name - Bool
                player.buff_type.pack_chat(self.display_name))    # Display Name - Chat

        #self.logger.info(", ".join(dir(self)))

        # Start sending "Keep Alive" packets
        self.ticker.add_loop(20, self.update_keep_alive)

        # Announce player joined
        self.factory.send_chat(u"\u00a7e%s has joined." % self.display_name)

    def player_left(self):
        ServerProtocol.player_left(self)

        # Send "Player List Item" packet
        for player in self.factory.players:
            player.send_packet("player_list_item",
                self.buff_type.pack_varint(4),                  # Action - 4: remove player - VarInt
                self.buff_type.pack_varint(1),                  # Number Of Players - VarInt
                self.buff_type.pack_uuid(self.uuid))            # UUID

        # Announce player left
        self.factory.send_chat(u"\u00a7e%s has left." % self.display_name)

    def update_keep_alive(self):
        # Send a "Keep Alive" packet

        # 1.7.x
        if self.protocol_version <= 338:
            payload =  self.buff_type.pack_varint(0)

        # 1.12.2
        else:
            payload = self.buff_type.pack('Q', 0)

        self.send_packet("keep_alive", payload)
        #self.logger.info("keep_alive")

    def packet_chat_message(self, buff):
        # When we receive a chat message from the player, ask the factory
        # to relay it to all connected players
        p_text = buff.unpack_string()
        
        if p_text.startswith('/'):
            self.send_packet("chat_message", self.buff_type.pack_chat(u"\u00a7cUnknown command") + self.buff_type.pack('B', 0) )
            return
        
        else:
            if p_text.startswith('>'): p_text = u"\u00a7a" + p_text
            self.factory.send_chat("<%s> %s" % (self.display_name, p_text))

class ChatRoomFactory(ServerFactory):
    protocol = Queue

    def send_chat(self, message):
        for player in self.players:
            player.send_packet("chat_message", player.buff_type.pack_chat(message) + player.buff_type.pack('B', 0) )

def main(argv):
    # Parse options
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--host", default="", help="address to listen on")
    parser.add_argument("-p", "--port", default=25565, type=int, help="port to listen on")
    parser.add_argument("-m", "--max", default=65535, type=int, help="player count")
    args = parser.parse_args(argv)

    # Create factory
    factory = ChatRoomFactory()
    factory.max_players = args.max
    factory.motd = u"\u00A74\u00A7l\u00A7o0B\u00A79\u00A7l\u00A7o0T\u00A7a\u00A7l\u00A7o.ORG\u00A7r \u00a78- offline or full \n\u00A76Aloha snackbar!"
    factory.online_mode = False
    factory.prevent_proxy_connections = False
    #factory.force_protocol_version = 340

    # Listen
    factory.listen(args.host, args.port)
    print ('Listening to ' + args.host + ':' + str(args.port) + '...' )
    reactor.run()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])