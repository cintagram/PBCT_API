"""Handler for Save Init"""
import BCSFE_Python_Discord
from typing import Optional, Any

class InvalidSaveError(Exception):
	pass

class TcCodeInvalidError(InvalidSaveError):
	pass

class SVFileCorruptedError(InvalidSaveError):
	pass
	
class InternalTkinterCrashedError(Exception):
	pass
	
class InvalidValueProvidedError(Exception):
	pass

class SaveManager:
	def __init__(self, mode: int, ev: Optional[int] = 2, country: Optional[str] = None, tc: Optional[str] = None, cc: Optional[int] = None, gv: Optional[str] = None, path: Optional[str] = None):
		"""
		Save Loader Class
		Parameters: 
		    mode: (required, type: int)
		        Configures how to load save.
		        1: download from transfer code
		        2: load from binary file(SAVE_DATA)
		        3: load from json file
		    ev: (Optional, type: int)
		        Editor version to use.
				2: [default] Use 2.7.2.3 version (BCSFE_Python_Discord), stable, recommanded.
		        3: Use 3.0.0 beta version (bcsfe), unstable since beta.
		    country: (mode1: Required, else: Ignored, type: str)
		        SaveData Country Code.
				Required when mode is 1.
				Should be in: kr/jp/tw/en.
		    tc: (mode1: Required, else: Ignored, type: str)
		        SaveData Transfer Code.
		        Required when mode is 1.
		    cc: (mode1: Required, else: Ignored, type: int)
		        SaveData Confirmation code(4-digit number).
				Required when mode is 1.
			gv: (mode1: Required, else: Ignored, type: str)
		        SaveData Game Version (ex: 12.7, 13.2.0, etc)
		        Required when mode is 1.
				Version under 11.0 is NOT supported.
		        Should be like: 12.7, 13.2.0, etc.
			path: (Optional, type: str)
		        In mode1: path where savefile will be saved.
				In other modes: path where savefile is located.
				If not given, Automatically show tkinter dialog which is not supported on cli platform or linux, phones.
				So give the path if you are using in Non-Supported platforms.
				
		Example: 
				SaveManager(mode=2, ev=2, path='/home/SAVE_DATA')
				SaveManager(mode=1, country='kr', tc='testestte', cc=1234, gv='13.2.0', path=r'C:\Users\user\Desktop\SAVE_DATA')
		"""
		global save_stats
		if isinstance(mode, int):
			loadmode_list = [1, 2, 3]
			if mode in loadmode_list:
				if mode == 1:
					if isinstance(country, str):
						self.country = country
					elif isinstance(country, None):
						raise TypeError("parameter <country> is required when parameter <mode> is 1.")
					else:
						raise TypeError(f"parameter <country> must be str, not {type(country)}.")
					if isinstance(tc, str):
						self.tc = tc
					elif isinstance(tc, None):
						raise TypeError("parameter <tc> is required when parameter <mode> is 1.")
					else:
						raise TypeError(f"parameter <tc> must be str, not {type(tc)}.")
					if isinstance(cc, int):
						self.cc = cc
					elif isinstance(cc, None):
						raise TypeError("parameter <cc> is required when parameter <mode> is 1.")
					else:
						raise TypeError(f"parameter <cc> must be int, not {type(cc)}.")
					if isinstance(gv, str):
						self.gv = gv
					elif isinstance(gv, None):
						raise TypeError("parameter <gv> is required when parameter <mode> is 1.")
					else:
						raise TypeError(f"parameter <gv> must be str, not {type(gv)}.")
					if isinstance(path, str):
						self.savepath = path
						self.tk_req = False
					elif isinstance(path, None):
						self.tk_req = True
					else:
						raise TypeError(f"parameter <path> must be str, not {type(path)}.")
						
					self.DownloadSaveData()

				if mode == 2 or mode == 3:
					if isinstance(path, str):
						self.savepath = path
						self.tk_req = False
					elif isinstance(path, None):
						self.tk_req = True
					else:
						raise TypeError(f"parameter <path> must be str, not {type(path)}.")
				if isinstance(ev, int):
					ev_list = [2, 3]
					if ev in ev_list:
						if ev == 2:
							self.edit_stable = True
							#self.LoadRawSaveFile()
						elif ev == 3:
							self.edit_stable = False
							#self.LoadJsonSaveFile()
					else:
						raise TypeError(f"parameter <ev> must be in {ev_list} when given, not {ev}.")
				else:
					raise TypeError(f"parameter <ev> must be int when given, not {type(ev)}.")
			else:
				raise TypeError(f"mode must be in {loadmode_list}.")
		else:
			raise TypeError(f"mode must be int, not {type(mode)}.")
			
			
	def DownloadSaveData(self):
		"""Downloading Save data"""
		if self.tk_req:
			self.savepath = helper.save_file(
				"Path where Save File will be stored",
                BCSFE_Python_Discord.helper.get_save_file_filetype(),
                BCSFE_Python_Discord.helper.get_save_path_home()
            )
		elif not self.tk_req:
			continue
		else:
			raise InternalTkinterCrashedError("Tkinter Protocol Crashed or path is not configured.")
		BCSFE_Python_Discord.helper.set_save_path(self.savepath)

		try:
			self.gv = BCSFE_Python_Discord.helper.str_to_gv(self.gv)
		except:
			raise InvalidValueProvidedError(f"Failed to Convert Provided gv '{self.gv}' to gv format.")

		try:
			save_data = BCSFE_Python_Discord.server_handler.download_save(self.country, self.tc, self.cc, self.gv)
		except:
			raise TcCodeInvalidError("Provided Transfer Information is not valid. Please check your info and try again.")

		try:
			save_data = BCSFE_Python_Discord.patcher.patch_save_data(save_data, self.country)
		except:
			raise SVFileCorruptedError("Failed to patch save data.")

		try:
			self.save_stats = BCSFE_Python_Discord.parse_save.start_parse(save_data, self.country)
		except:
			raise SVFileCorruptedError("Failed to parse save data.")
		if save_stats == 0: #save stats is empty
			raise SVFileCorruptedError("Failed to parse save data")
		else:
			continue

		BCSFE_Python_Discord.edits.save_management.save.save_save(self.save_stats)
		return self.save_stats
