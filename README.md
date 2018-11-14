# Chinese Segmentation Tool

This poject is a segmentation tool for Chinese text. It uses a combination of Forward Maximum Matching (FMM) and 
Reverse Maximum Matching (RMM) followed by a lowest-mean-cost disambiguation algorithm.

## Requirements

* Python version: 3.5.1

## Start Developing

After cloning the repository, run the program:

* Setting up the environment：
    - `cd chinese-segmentation-tool`
    - Create a virtual environmnet: `python3 -m venv virtual-environment`
    - `cd virtual-environment/bin`
    - Enter `source activate` to start the virtual environment
    - `cd ../..` (to return to the `chinese-segmentation-tool` folder)
    - Install the project dependencies：`pip install –r requirements.txt`

* Start the program:
    - Ensure that you are inside `chinese-segmentation-tool` and that your virtual environment is running
    - Enter `python __main__.py`
    - Following the prompt in the terminal, enter a Chinese sentence. The program will then output the results.
    - To stop the program, enter `1`.
    - Deactivate your virtual environment by entering `deactivate`
