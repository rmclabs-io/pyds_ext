from distutils.core import setup
setup (name = 'pyds_metadata_patch',
       version = '1.0',
       description = """Install precompiled DeepStream Python bindings for tracker metadata extension""",
       packages=[''],
       package_data={'': ['pyds_tracker_meta.so', 'pyds_bbox_meta.so']},
       )
