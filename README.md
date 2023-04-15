# Surveillance Camera for Cashier
This project is a surveillance camera system that detects when a cashier raises their hands in response to a potential threat, and sends an alert message with the exact GPS coordinates to a designated recipient via the Telegram API and also stores the culprit image in database as well it will create logs. The system also includes a feature to detect when someone approaches the camera at a certain point.
* [Watch the video here 👆](https://www.linkedin.com/posts/activity-6941673746109714432-XHKC?utm_source=share&utm_medium=member_desktop)
## Requirements
* Python 3.x
* Mediapipe 0.8.6 or higher
* OpenCV 4.x
* NumPy
* TensorFlow 2.x
* SpeechRecognition
* PyAudio
* PyTelegramBotAPI
## Installation
1. Clone the repository to your local machine. 
 ```python 
    git clone https://github.com/your-username/surveillance-camera.git
 ``` 
2. Install Python 3.x if you haven't already done so. You can download it from the official website: https://www.python.org/downloads/
3. Install the required Python packages using pip. Open a terminal or command prompt and navigate to the project directory. Then, run the following command:
```python 
pip install -r requirements.txt
``` 
4. Download and install the TensorFlow Object Detection API by following the instructions on this page: https://tensorflow-object-detection-api-tutorial.readthedocs.io/en/latest/install.html
5. Download the pre-trained MediaPipe hand detection model from the following link and save it to the project directory: https://drive.google.com/file/d/1IwD10jKmFg8MnmOHMtnmF_iCQl06OZvo/view?usp=sharing
6. Create a Telegram bot and obtain its API key by following the instructions on this page: https://core.telegram.org/bots#creating-a-new-bot
7. Add the bot to a group or channel and obtain its chat ID by following the instructions on this page: https://sean-bradley.medium.com/get-telegram-chat-id-80b575520659
8. Open the 'config.py' file and replace the 'BOT_TOKEN' and 'CHAT_ID' variables with your Telegram bot API key and chat ID.
## Usage
1. Navigate to the project directory and run the following command in a terminal or command prompt:
```python 
python main.py
```
2. The program will start running and the camera will start capturing frames. If a cashier raises their hands, the program will detect it and start a 10-second timer. If the cashier does not lower their hands within 10 seconds, the program will use the SpeechRecognition package to transcribe any speech in the vicinity of the camera and determine whether or not the cashier is in danger based on an NLP model.
3. If the program determines that the cashier is in danger, it will send a message to the designated Telegram chat with the exact GPS coordinates of the camera.
4. If a person approaches the camera at a certain point, the program will detect it and log the event in a text file.
# References
* Mediapipe: https://mediapipe.dev/
* TensorFlow Object Detection API: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2.md
* PyTelegramBotAPI documentation: https://github.com/eternnoir/pyTelegramBotAPI/blob/master/README.md
