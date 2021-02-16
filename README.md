# pyds_custom_meta

[pybind11](https://github.com/pybind/pybind11) wrapper to access Nvidia
[DeepStream](https://developer.nvidia.com/deepstream-sdk) metadata from Python.

* Tracker meta info (`NvDsPastFrame...` classes)
* Detector and tracker bbox info (`NvDsObjectMeta.[tracker/detector]_bbox_info...` attrs) from Python.
* Also install default `pyds` precompiled library from `/opt/nvidia/deepstream/deepstream/lib`

## Installation


### Prerequisites

1. python3.6
1. Deepstream v5
1. [Option A] [pep-517](https://www.python.org/dev/peps/pep-0517/) compatible pip:

   ```console
   pip install "pip>=10"
   ```

1. [Option B] Only necessary for old `pip<10`:
   * [pybind11](https://github.com/pybind/pybind11):
     * [Option B.1] You might try simply `pip install pybind11`.
     * [Option B.2] The recommended way is to [build it from source](https://pybind11.readthedocs.io/en/stable/basics.html?highlight=install#compiling-the-test-cases)

### Install package

```console
pip install --upgrade pip>=10
pip install git+https://github.com/rmclabs-io/pyds_custom_parser.git
```

## Usage

This meta-package provides three packages:

1. `pyds`: Standard pyds from `/opt/nvidia/deepstream/deepstream/lib`.
2. pyds_object_meta: Enable `NvDsObjectMeta.tracker_bbox_info...` and `NvDsObjectMeta.detector_bbox_info...` access.
3. pyds_tracker_meta: Enable `NvDsPastFrame...` access.

### Standard pyds

See oficial documentation [here](https://github.com/NVIDIA-AI-IOT/deepstream_python_apps)

### Object metadata

Use the following as a reference to extract bbox metadata:

```python
import pyds_bbox_meta

def osd_sink_pad_buffer_probe(pad, info, u_data):

    # ... code to acquire frame_meta
    l_obj=frame_meta.obj_meta_list
    while l_obj is not None:
        try:
            obj_meta=pyds_bbox_meta.NvDsObjectMeta.cast(l_obj.data)
        except StopIteration:
            break
        tracker_width = obj_meta.tracker_bbox_info.org_bbox_coords.width
        detector_width = obj_meta.detector_bbox_info.org_bbox_coords.width
        print(f"tracker_width: {tracker_width}")
        print(f"detector_width: {detector_width}")
        try: 
            l_obj=l_obj.next
        except StopIteration:
            break
        ...
```

### Tracker metadata

Ensure you have set `enable-past-frame` property of the `gst-nvtracker` plugin to `1`.
(See [nvtracker](https://docs.nvidia.com/metropolis/deepstream/dev-guide/#page/DeepStream%20Plugins%20Development%20Guide/deepstream_plugin_details.3.02.html#) plugin documentation.)

Use the following as a reference to extract tracker metadata:

```python
import pyds_tracker_meta

def osd_sink_pad_buffer_probe(pad, info, u_data):
    
    # ... code to acquire batch_meta
    
    user_meta_list = batch_meta.batch_user_meta_list
    while user_meta_list is not None:
        user_meta = pyds.NvDsUserMeta.cast(user_meta_list.data)
        
        print('user_meta:', user_meta)
        print('user_meta.user_meta_data:', user_meta.user_meta_data)
        print('user_meta.base_meta:', user_meta.base_meta)
        
        if user_meta.base_meta.meta_type != pyds.NvDsMetaType.NVDS_TRACKER_PAST_FRAME_META:
            continue
            
        pfob = pyds_tracker_meta.NvDsPastFrameObjBatch_cast(user_meta.user_meta_data)
        print('past_frame_object_batch:', pfob)
        print('  list:')
        for pfos in pyds_tracker_meta.NvDsPastFrameObjBatch_list(pfob):
            print('    past_frame_object_stream:', pfos)
            print('      streamID:', pfos.streamID)
            print('      surfaceStreamID:', pfos.surfaceStreamID)
            print('      list:')
            for pfol in pyds_tracker_meta.NvDsPastFrameObjStream_list(pfos):
                print('        past_frame_object_list:', pfol)
                print('          numObj:', pfol.numObj)
                print('          uniqueId:', pfol.uniqueId)
                print('          classId:', pfol.classId)
                print('          objLabel:', pfol.objLabel)
                print('          list:')
                for pfo in pyds_tracker_meta.NvDsPastFrameObjList_list(pfol):
                    print('            past_frame_object:', pfo)
                    print('              frameNum:', pfo.frameNum)
                    print('              tBbox.left:', pfo.tBbox.left)
                    print('              tBbox.width:', pfo.tBbox.width)
                    print('              tBbox.top:', pfo.tBbox.top)
                    print('              tBbox.right:', pfo.tBbox.height)
                    print('              confidence:', pfo.confidence)
                    print('              age:', pfo.age)
        try:
            user_meta_list = user_meta_list.next
        except StopIteration:
            break
```

NOTE: see [pythia](https://github.com/rmclabs-io/pythia.git) for an easy-to-use API.

## References

* [tracker patch](https://forums.developer.nvidia.com/t/how-to-access-past-frame-tracking-results-from-python-in-deepstream-5-0/155245/5)
   repo also available [here](https://github.com/mrtj/pyds_tracker_meta)
* [bbox patch](https://forums.developer.nvidia.com/t/deepstream-5-0-python-api/158762/4)
