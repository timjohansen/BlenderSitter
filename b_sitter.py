import argparse, math, time, subprocess, shlex, atexit
from pathlib import Path


class RenderProc:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog='Blender Render Monitor',
            description='A program that launches and monitors Blender while it renders an animation.')
        parser.add_argument('executable')
        parser.add_argument('project')
        parser.add_argument('-o', '--render-output', required=True)
        parser.add_argument('-s', '--frame-start', required=True)
        parser.add_argument('-e', '--frame-end', required=True)
        parser.add_argument('-t', '--timeout', default='0')
        args = parser.parse_args()

        self.proc = None
        self.path_to_app = Path(args.executable)
        self.path_to_project_file = Path(args.project)
        self.path_to_output = Path(args.render_output)
        self.filename = self.path_to_output.parts[len(self.path_to_output.parts) - 1]
        self.start_frame = int(args.frame_start)
        self.end_frame = int(args.frame_end)
        self.current_frame_num = self.start_frame
        self.seconds_to_timeout = int(args.timeout)
        self.timeout_base = 0
        self.prev_frame_time = 0
        self.kill_proc_func = self.kill_proc

    def start_proc(self):
        digits = int(math.log10(self.end_frame) + 1)
        filename_with_digits = self.filename
        for i in range(digits):
            filename_with_digits += "#"

        command = shlex.split(
            shlex.quote(str(self.path_to_app)) + " --background " + shlex.quote(str(self.path_to_project_file)) +
            " --render-output " + shlex.quote(str(self.path_to_output)) + " -s " + str(self.current_frame_num) +
            " -e " + str(self.end_frame) + " --render-anim")
        new_proc = subprocess.Popen(command, stdout=subprocess.DEVNULL)
        return new_proc

    def main(self):
        self.timeout_base = time.time()
        self.prev_frame_time = time.time()

        print("Starting process, rendering frames " + str(self.start_frame) + " to " + str(self.end_frame))
        self.proc = self.start_proc()

        while self.current_frame_num <= self.end_frame:

            # Check if process is still running
            if self.proc.poll() is not None:
                # If not, restart and continue.
                print('Process crash detected. Restarting process at frame ' + str(self.current_frame_num))
                self.proc = self.start_proc()
                self.timeout_base = time.time()
                continue

            # Check the output folder for the current frame
            time.sleep(2)
            done = False
            while not done:
                # Determine what the filename of the next frame will be.
                current_frame_filename = self.filename
                if self.end_frame > 0:
                    total_num_of_digits = int(math.log10(self.end_frame) + 1)
                else:
                    total_num_of_digits = 1
                if self.current_frame_num > 0:
                    current_num_of_digits = int(math.log10(self.current_frame_num) + 1)
                else:
                    current_num_of_digits = 1
                leading_zeros = total_num_of_digits - current_num_of_digits
                for i in range(leading_zeros + 1):
                    current_frame_filename += "0"

                current_frame_filename += str(self.current_frame_num)
                file_found = False

                # Checks the name and modified time of every file in the directory. If the name matches the previously
                # calculated name, and was modified later than the previous frame, the frame was successfully rendered.
                # Increment the counter and repeat until we're caught up.
                for item in self.path_to_output.parent.iterdir():
                    if item.is_file():
                        item_name = item.stem.lower()
                        item_mtime = item.stat().st_mtime
                        if item_name == current_frame_filename and item_mtime >= self.prev_frame_time:
                            print("Frame " + str(self.current_frame_num) + " complete")
                            file_found = True
                            self.current_frame_num += 1
                            self.prev_frame_time = item_mtime
                            self.timeout_base = time.time()
                if not file_found:
                    # If another frame hasn't been completed yet, we move on.
                    done = True

            # Check if the current frame is taking too long and restart if necessary.
            if self.seconds_to_timeout > 0 and time.time() - self.timeout_base >= self.seconds_to_timeout:
                print("Frame timed out. Restarting process at frame " + str(self.current_frame_num))
                self.kill_proc()
                time.sleep(3)
                self.proc = self.start_proc()
                self.timeout_base = time.time()

        print("Render complete!")

    def kill_proc(self):
        self.proc.kill()


render = RenderProc()
atexit.register(render.kill_proc)
render.main()