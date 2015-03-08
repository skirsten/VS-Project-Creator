## Visual Studio Project Creator
This python script creates Visual Studio projects for you! 
The created projects feature:
- Clean build environment
- Auto include the correct `.lib` files for the current build target
- Auto copy the correct `.dll`´s to the bin directory
 
Generated folder structure:
- `bin` Here are several subdirectorys generated after build that contain your final `exe`´s
- `build` Internal Visual Studio stuff. *just ignore it ;)*
- `include` Here are your header files stored
- `lib` In the two subdirectories coresponding to the different build targets you can put your additional `.lib`´s and `.dll`´s. Note: The`.dll`´s are automatically copied to the right `bin` directory so don´t worry.
  - `x64` 
  - `x86`
- `run` In this folder, the programm is run by Visual Studio. Put files that the Project uses while running there but no dll´s
- `src` Here comes your code


## Requirements
- python 2.7 or 3.4 (should work with all modern versions)

# Usage
## Windows
Run `createproject.bat` in the folder you want the project to be created or just double click it and move the folder afterwards.
You will be prompted with the project´s name.
## Linux
Run `createproject.sh` in the folder you want the project to be created.
You will be prompted with the project´s name.
## Other (using python)
Run `python createproject.py [project name]` in the folder you want the project to be created.
