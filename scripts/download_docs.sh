root_dir=$(realpath $(dirname $(realpath $0))/..)
docs_dir="${root_dir}/docs"

base_url="https://help.autodesk.com/cloudhelp/2026/ENU/Flame-API/files/Python-API/autodesk-flame-python-api/"

pages=(
    Flame_API_Python_API_autodesk_flame_python_api_html
    Flame_API_Python_API_autodesk_flame_python_api_Action_Nodes_Attributes_html
    Flame_API_Python_API_autodesk_flame_python_api_Batch_Nodes_Attributes_html
    Flame_API_Python_API_autodesk_flame_python_api_PyActionNode_html
    Flame_API_Python_API_autodesk_flame_python_api_PyAudioTrack_html
    Flame_API_Python_API_autodesk_flame_python_api_PyBatch_html
    Flame_API_Python_API_autodesk_flame_python_api_PyBatchIteration_html
    Flame_API_Python_API_autodesk_flame_python_api_PyClip_html
    clip_node_attributes
    Flame_API_Python_API_autodesk_flame_python_api_PyCoCompass_html
    Flame_API_Python_API_autodesk_flame_python_api_PyCompassNode_html
    Flame_API_Python_API_autodesk_flame_python_api_PyDesktop_html
    Flame_API_Python_API_autodesk_flame_python_api_PyFolder_html
    Flame_API_Python_API_autodesk_flame_python_api_PyLibrary_html
    lens_distortion_python_attributes
    Flame_API_Python_API_autodesk_flame_python_api_PyMarker_html
    type_python_pymediahub
    type_python_pymediahubtab
    type_python_pymediahubfilestab
    type_python_pymediahubfilestaboptions
    Flame_API_Python_API_autodesk_flame_python_api_PyNode_html
    Flame_API_Python_API_autodesk_flame_python_api_PyOFXNode_html
    Flame_API_Python_API_autodesk_flame_python_api_PyPaintNode_html
    Flame_API_Python_API_autodesk_flame_python_api_PyProject_html
    Flame_API_Python_API_autodesk_flame_python_api_PyReel_html
    Flame_API_Python_API_autodesk_flame_python_api_PyReelGroup_html
    Flame_API_Python_API_autodesk_flame_python_api_PySegment_html
    Flame_API_Python_API_autodesk_flame_python_api_PySequence_html
    Flame_API_Python_API_autodesk_flame_python_api_PyTimelineFX_html
    timewarp_python_attributes
    Flame_API_Python_API_autodesk_flame_python_api_PyTrack_html
    type_python_attributes
    Flame_API_Python_API_autodesk_flame_python_api_PyVersion_html
    Flame_API_Python_API_autodesk_flame_python_api_PyWorkspace_html
    )

for page in "${pages[@]}"; do
    wget $base_url/$page.html -O $docs_dir/$page.html
done
