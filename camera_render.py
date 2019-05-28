# A two-wheeled robot that tries to avoid walls using sensors
# Scene File: ss_pioneer.ttt
import nengo
import sensors
import actuators
from robots import CustomRobot
from functools import partial

from nengo_extras.gui import image_display_function

model = nengo.Network(label="Pioneer p3dx", seed=13)

# Create a robot object that can have sensors and actuators added to it
# The 'sim_dt' parameter is the dt it is expecting V-REP to be run with
# this can be different than Nengo's dt and the difference is accounted
# for when the two simulators are set to be synchronized
robot = CustomRobot(sim_dt=0.05, nengo_dt=0.001, sync=True)

# When adding sensors and actuators, the string names given must match
# the names of the specific sensors and actuators in V-REP
# These names can be found in the Scene Hierarchy pane

robot.add_sensor('Vision_sensor',
                partial(sensors.rgb_vision, width=32, height=32, grayscale=False), dim=32*32*3)
robot.add_actuator("Revolute_joint", actuators.joint_velocity)

model.config[nengo.Ensemble].neuron_type=nengo.LIF()
image_shape = (3, 32, 32)
with model:
  # Create a Node that interfaces Nengo with V-REP
  robot_node = robot.build_node()
  # the above function is just a shortcut for the following line
  #robot = nengo.Node(pioneer, size_in=2, size_out=8)
  
  u = nengo.Node(size_in=32*32*3)
  nengo.Connection(robot_node, u, synapse=None)
  
  #u = nengo.Node(nengo.processes.PresentInput(images, 0.1))
  display_f = image_display_function(image_shape)
  display_node = nengo.Node(display_f, size_in=u.size_out)
  nengo.Connection(u, display_node, synapse=None)