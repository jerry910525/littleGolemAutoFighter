# Little golem AutoFighter
## Abstract
The project can connect the computing-end from CGI server to little golem website to achieve auto-fighting process. Due to technical issue, it still has a lot of pre-requirement or restrictions. If one of them doesent meet, it might not work.

 
## Requirement
1. An Windows 10 system with 1920x1080 resolution.
2. MobaXterm with bright color theme.
3. An Container that can be connected to in order to compute the move.
4. Python enviroment(my version is 3.11.5)
5. Chrome or other browser's driver for automated test.

## Usage
1. Prepare the python enviroment with all packages installed(requirement.txt).
2. Type in your account information in main.py.
3. Open the mobaxterm and set the theme to "windows bright theme". Also, set the directory for saving terminal output to "autoLG/moba".
![image](https://hackmd.io/_uploads/SyFjHZAiT.png)

4. Prepare all the  stuffs(mobaXterm, container, program, model to be tested)and make sure they are ready to be executed. For example, execute "python3 -m clap.tool.CLI_agent -r -game slither -model ../02525_6.pt -count 400". Here we add "-r" to avoid our program from termination when one of the game has ended.
5. Run "main.py" and it should start working.

## Debugging
Since this is a poor project, it has great chance to stop working. You might want to check followings.
1. It does not sleep enough.(previous command has not finished yet).
2. It can't locate where "save terminal output" is. You might want to change the confident for recognizing images(see comments also)
3. It not able to control MobaXterm window. Sometimes it just happens and I DON'T KNOW why either. Usually, restart mobaXterm can fix it.

## Deploy it on Windows RDP
You can use Task Scheduler to run "dis.bat" periodically to simulate a new user take over the connection instead of disconnecting from original user.
