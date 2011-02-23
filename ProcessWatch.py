import sys
import os
import subprocess
import re

class ProcessWatch:
  def __init__(self, agentConfig, checksLogger, rawConfig):
    self.agentConfig = agentConfig
    self.checksLogger = checksLogger
    self.rawConfig = rawConfig

  def run(self):
    data = {}
    for p in ["delayed_job", "thin"]: # put whatever process names you wish to monitor here
      if self.isThisRunning(p) == False:
        data[p] = 0 # not running
      else:
        data[p] = 80 # running!

    return data

  def findThisProcess(self, process_name):
    ps = subprocess.Popen("ps -eaf | grep "+process_name+" | grep -v grep", shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()

    return output

  # This is the function you can use
  def isThisRunning(self, process_name):
    output = self.findThisProcess(process_name)

    if re.search(''+process_name, output) is None:
      return False
    else:
      return True