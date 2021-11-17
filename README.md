# Social Interaction with Pepper Robot using Human Emotion Recognition
Project repository for the course of Human Robot Interaction 2021, Sapienza University of Rome. 

## Abstract
Humanoid robots are becoming more and more a thing close to reality rather than just an image of the future. This is thanks to huge recent technology improvements, especially in the field of Artificial Intelligence (AI). Thanks to AI it is possible to build autonomous systems that are able to interact with people, helping them in different manners. In the scenario of Human-Robot Interaction (HRI) I propose a small simulation project, in which the interaction happens according to emotions.

## The project
The Python project implementation includes different modules for allowing a simulated interaction between the Pepper Robot and a Human (through the terminal):
- **application.py**: main application flow, which represents the high level interaction.
- **pepper.py**: high level functions which perform some high level robot behaviours.
- **fer.py**: face emotion recognition system implemented in tensorflow.
- **server.py**: flask Server used to play a simple true or false game (simulating the Pepper tablet). The relative templates are in the homonymous folder.
- **human_say.py** and **touch_sim.py**: python scripts used as communication methods from human to Pepper robot.

### Requirements
#### modules
- tensorflow
- naoqi 2.5
- cv2
- requests
- numpy

### operating system
Ubuntu 16

### simulation environment
Choregraphe (Softbank)

### extra
The project needs support for naoqi 2.5 (Python libraries) which has been discontinued by SoftBank.

## [Video](https://youtu.be/lU1Jm5o9DDM)
## [Report](https://github.com/Starnino/hri_project/blob/main/HRI_Report.pdf)

## References
> Softbank Robotics
[Naoqi Developer Guide](http://doc.aldebaran.com/2-5/index_dev_guide.html)
