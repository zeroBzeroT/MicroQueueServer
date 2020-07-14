# Stonewall
Minecraft server and velocity plugin that act as an efficient queue system. The server (Stonewall) acts as very simple Minecraft server, only sending the bare minimum to keep the client connected. The queue plugin (VelocityQueue) is a Velocity plugin that implements a 2b2t-style queue system.

## Installation

#### Stonewall
Run the `stonewall.py` script in a terminal. Run `./stonewall.py -h` for argument info.

#### VelocityQueue
Cd into the `velocityqueue` folder and run `mvn install`, the built plugin will be in `target`. You can then put the jar into the plugin folder of your Velocity install and run Velocity. A config file will be generated on first run which you can modify to suit your needs.
