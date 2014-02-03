import os
import sublime
import sublime_plugin
import threading
import subprocess
import functools
import os.path
import time
import re


class RunBuildCvsCommand(sublime_plugin.WindowCommand):
    # helper
    #  * for setting the build_system
    #  * running build
    #  * and then resetting the build_system to automatic
    def run(self, build_system, build_variant):
        self.window.run_command( "set_build_system", {"file": build_system } )
        self.window.run_command( "build", {
            "variant": build_variant
        })
        self.window.run_command("set_build_system", {"file":""}) # Set build_system to *automatic*

class QuickCvsCommitBuildTargetCommand(sublime_plugin.WindowCommand):
    def run(self, cmd = [], file_regex = "", line_regex = "", working_dir = "", encoding = "utf-8", env = {}, path = "", shell = False):
        self.execDict = {
            "path" : path,
            "shell" : shell,
            "cmd" : cmd,
            "file_regex" : file_regex,
            "line_regex" : line_regex,
            "working_dir" : working_dir,
            "encoding" : encoding,
            "env" : env
        }
        self.window.show_input_panel("Commit message", "", self.on_done, None, None)
    def on_done(self, message):
        self.execDict["cmd"][3] = message
        self.window.run_command('exec', self.execDict)




def cvs_root(directory):
    retval = False

    if os.path.exists(os.path.join(directory, 'CVS')):
        retval = directory

    return retval



class QuickCvsBranchStatusListener(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        view.run_command("quick_cvs_branch_status")

    def on_post_save_async(self, view):
        view.run_command("quick_cvs_branch_status")

    def on_load_async(self, view):
        view.run_command("quick_cvs_branch_status")


class QuickCvsBranchStatusCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        s = sublime.load_settings("QuickCVS.sublime-settings")
        if s.get("cvs_statusbar"):
            full_file_name = self.view.file_name()

            if not full_file_name:
                # e.g. a view which wasn't saved yet
                return

            file_name = os.path.basename(full_file_name)
            file_path = os.path.dirname(full_file_name)

            if not os.path.exists(os.path.join(file_path, 'CVS')):
                # non-CVS folder
                return

            p = subprocess.Popen(['cvs status ' + file_name], cwd=file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result = p.communicate()
            self.branchstatus(result)
        else:
            self.view.set_status("cvs-branch", "")
            self.view.set_status("cvs-status", "")

    def branchstatus(self, result):

        output = result[0].decode("utf-8")
        error = result[1].decode("utf-8")

        if error:
            print("cvs error: " + error)
            self.view.set_status("cvs-branch", "")
            self.view.set_status("cvs-status", "")
            return

        lines = output.splitlines()

        if len(lines) <= 2:
            # something's wrong
            self.view.set_status("cvs-branch", "")
            self.view.set_status("cvs-status", "")
            return

        branch = ""
        status = ""

        m = re.compile(r".*?Status:\s+([a-zA-Z -]*)").match(lines[1])
        if m:
            status = m.group(1).strip()

            if status == "Unknown":
                # new cvs file in a cvs-controlled folder
                self.view.set_status("cvs-branch", "CVS status: new file or unknown")
                self.view.set_status("cvs-status", "")
                return
        else:
            # something's wrong
            self.view.set_status("cvs-branch", "")
            self.view.set_status("cvs-status", "")
            return

        m = re.compile(r".*?Sticky Tag:\s+(\S*)").match(lines[7])
        if m:
            branch = m.group(1).strip()
            if branch == "(none)" or branch == "":
                branch = "HEAD"

        self.view.set_status("cvs-branch", "CVS branch: " + branch)
        self.view.set_status("cvs-status", "status: " + status)

