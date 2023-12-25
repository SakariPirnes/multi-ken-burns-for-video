import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
                                                                                 
setuptools.setup(
    name='multikb',
    version='0.0.1',
    author='Sakari Pirnes',
    author_email='sakaripirnes@gmail.com',
    description='nice stuff',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['multikb'],
    entry_points = {
    "console_scripts" : ["multikb=multikb.console_scripts:main_script",
        "multikb_get_cropped_frames=multikb.console_scripts:get_cropped_frames_script",
        "multikb_console_scripts=multikb.console_scripts:connect_cropped_frames_script",
        "multikb_video_from_connected_cropped_frames=multikb.console_scripts:video_from_connected_cropped_frames_script"]
    }
)
