class Setting:
    def __init__(self):
        self.quality = ""
        self.idm_download = False    
        self.idm_start = False

    def resetSetting(self):
        self.quality = ""
        self.idm_download = False
        self.idm_start = False
        print(f"setting Reseted \"{self.quality}\" {self.idm_download} {self.idm_start}")
    def __str__(self):
        return f"Settings : \"{self.quality}\" - add to queue:{self.idm_download} - start now:{self.idm_start}"
