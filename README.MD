# BlenderSitter

Inspired by many wasted hours and overnight renders, BlenderSitter is a simple Python app for monitoring Blender while it renders 3D animations. 
If it detects that Blender has crashed, it will restart the process and continue the render from the last completed frame without needing any user input.

The app monitors in two ways. First, it checks if the Blender process is still running, and restarts it if not. Second, it watches the output folder as the render
progresses, and if it ever takes too long for a frame to appear, it restarts. 


WARNING: This script is still early in development. It has very little error handling, has only been tested on MacOS, 
and should be treated as a proof of concept for now. Don't use it for anything important, and if you do, you do so at your own risk.

## Requirements
Any recent-ish version of Python should work. Note that this script **is not** a Blender addon and must be launched from outside of Blender.

## Usage
b_sitter.py [Blender path] [.blend path] [-o] output [-s] startframe [-e] endframe [-t] seconds

### Options

**Blender path**: The path to the Blender executable. Note that on Macs, the executable is hidden inside Blender.app. \
&emsp;&emsp; Example: "/Applications/Blender.app/Contents/MacOS/Blender" 

**.blend path**: The path to the .blend project file. 

**output** : Path to the output directory, including the filename \
&emsp;&emsp; Example: -o /Users/Tim/Desktop/Output/frame 

**-s startframe**: Start of range of frames to render \
&emsp;&emsp; Example: -s 0 

**-e endframe** : End of range of frames to render \
&emsp; &emsp; Example: -e 150 

**-t seconds**: How many seconds to wait for a frame to finish before restarting. Omitting this option will disable the timer.\
&emsp; &emsp; Example: -t 60

# TODO List

* Ensure it works on Windows and do some stress testing. I haven't used this for a "real" project yet.
* Build a GUI with frame previews, progress bars, and that type of fun stuff.
* Add support for more Blender command line arguments.
* Provide default locations to search for the Blender application, or have a way to save the location.
* Integrate Blender's 'blend_render_info.py' to automatically get the frame range from the project file.
* Add support for other applications, or at least make it easier for users to reconfigure the script for their app of choice. 