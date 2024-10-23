import os,platform,subprocess,sys
def set_playwright_browsers_path(custom_path):
	'Sets the PLAYWRIGHT_BROWSERS_PATH environment variable based on OS';C='PLAYWRIGHT_BROWSERS_PATH';A=custom_path;B=platform.system()
	if B=='Windows':os.environ[C]=A;print(f"Set PLAYWRIGHT_BROWSERS_PATH to {A} on Windows")
	elif B=='Darwin':os.environ[C]=A;print(f"Set PLAYWRIGHT_BROWSERS_PATH to {A} on macOS")
	else:print(f"Unsupported OS: {B}");return False
	return True
def install_chromium():
	'Runs the playwright install chromium command'
	try:subprocess.run(['python','-m','playwright','install','chromium'],check=True);print('Chromium installation successful!')
	except subprocess.CalledProcessError as A:print(f"Error occurred during Chromium installation: {A}")
if __name__=='__main__':
	python_executable_dir=os.path.dirname(sys.executable);custom_browser_path=python_executable_dir
	if set_playwright_browsers_path(custom_browser_path):install_chromium()