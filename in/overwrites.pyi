"""(semi) Handwritten type overlays applied on top of auto-generated Flame stubs."""

from typing import Any

class PresetType:
    Audio: PresetType
    Distribution_Package: PresetType
    Image_Sequence: PresetType
    Movie: PresetType
    Sequence_Publish: PresetType

class PresetVisibility:
    Autodesk: PresetVisibility
    Flow_Production_Tracking: PresetVisibility
    Project: PresetVisibility
    Shared: PresetVisibility
    Shotgun: PresetVisibility
    User: PresetVisibility

class PyInferenceNode(PyNode):
    model_name: str

class PyActionFamilyNode:
    attributes: list[PyAttribute]
    cursor_position: tuple[float, float]
    input_sockets: list[str]
    media_layers: list[PyNode]
    node_types: list[str]
    nodes: list[PyNode]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    def create_node(
        arg1: PyActionFamilyNode,
        node_type: str,
        file_path: str = "",
        is_udim: bool = False,
        tile_resolution: int = 0,
        input_colour_space: str = "",
    ) -> PyNode: ...
    def get_node(arg1: PyActionFamilyNode, node_name: str) -> PyNode: ...
    def encompass_nodes(arg1: PyActionFamilyNode, node_list: list) -> PyCoCompass | PyCompassNode: ...

class PyActionNode:
    attributes: list[PyAttribute]
    cursor_position: tuple[float, float]
    input_sockets: list[str]
    media_layers: list[PyNode]
    media_nodes: list[PyNode]
    node_types: list[str]
    nodes: list[PyNode]
    output_sockets: list[str]
    output_types: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    def create_node(
        arg1: PyActionFamilyNode,
        node_type: str,
        file_path: str = "",
        is_udim: bool = False,
        tile_resolution: int = 0,
        input_colour_space: str = "",
    ) -> PyNode: ...
    def get_node(arg1: PyActionFamilyNode, node_name: str) -> PyNode: ...
    def encompass_nodes(arg1: PyActionFamilyNode, node_list: list) -> PyCoCompass | PyCompassNode: ...

class PyArchiveEntry:
    attributes: list[PyAttribute]
    parent: PyFlameObject

class PyAttribute:
    values: list[Any]

class PyAudioTrack:
    attributes: list[PyAttribute]
    channels: list[Any]
    parent: PyFlameObject
    stereo: bool
    def copy_to_media_panel(
        arg1: PyAudioTrack, destination: PyArchiveEntry, duplicate_action: str = "add"
    ) -> PyClip: ...

class PyBatch:
    attributes: list[PyAttribute]
    batch_iterations: list[PyBatchIteration]
    contexts: dict[int, Any]
    current_iteration: PyBatchIteration
    current_iteration_number: int
    cursor_position: tuple[float, float]
    node_types: list[str]
    nodes: list[PyNode]
    opened: bool
    parent: PyFlameObject
    reels: list[PyReel]
    shelf_reels: list[PyReel]
    def create_batch_group(
        arg1: PyBatch,
        name: str,
        nb_reels: Any = None,
        nb_shelf_reels: Any = None,
        reels: list = None,
        shelf_reels: list = None,
        start_frame: int = 1,
        duration: Any = None,
    ) -> PyBatch: ...
    def create_reel(arg1: PyBatch, name: str) -> PyReel: ...
    def create_shelf_reel(arg1: PyBatch, name: str) -> PyReel: ...
    def create_node(arg1: PyBatch, node_type: str, file_path: str = "") -> PyNode: ...
    def get_node(arg1: PyBatch, node_name: str) -> PyNode: ...
    def encompass_nodes(arg1: PyBatch, nodes: list) -> PyCompassNode: ...
    def iterate(arg1: PyBatch, index: int = -1) -> PyBatchIteration: ...
    def save(arg1: PyBatch) -> PyBatchIteration: ...
    def save_current_iteration(arg1: PyBatch) -> PyBatchIteration: ...
    def import_clip(arg1: PyBatch, file_path: str, reel_name: str) -> PyClip: ...
    def import_clips(arg1: PyBatch, file_paths: Any, reel_name: str) -> list[PyClip]: ...

class PyBatchIteration:
    attributes: list[PyAttribute]
    iteration_number: int
    parent: PyFlameObject

class PyBrowser:
    bit_depth: str | None
    colour_space: str
    frame_ratio: float | None
    height: int | None
    resize_filter: str
    resize_mode: str
    resolution: str
    scaling_presets_value: float | None
    scan_mode: str
    selection: list[str]
    sequence_mode: str
    width: int | None

class PyClip:
    archive_date: str
    archive_error: str
    attributes: list[PyAttribute]
    audio_tracks: list[PyAudioTrack]
    bit_depth: str
    cached: bool
    colour_primaries: str
    creation_date: str
    duration: PyTime
    essence_uid: str
    frame_rate: str
    has_deliverables: bool
    has_history: bool
    height: int
    markers: list[PyMarker]
    matrix_coefficients: str
    original_source_uid: str
    parent: PyFlameObject
    proxy_resolution: str
    ratio: float
    sample_rate: str
    scan_mode: str
    source_uid: str
    start_frame: int
    subtitles: list[PySubtitleTrack]
    transfer_characteristics: str
    unlinked: bool
    versions: list[PyVersion]
    width: int
    def create_marker(arg1: PyClip, location: Any) -> PyMarker: ...
    def open_as_sequence(arg1: PyClip) -> PySequence: ...

class PyClipNode:
    attributes: list[PyAttribute]
    clip: PyClip | PySequence
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    version_uid: str
    version_uids: list[str]

class PyClrMgmtNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyCoCameraAnalysis:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    type: str

class PyCoCompass:
    attributes: list[PyAttribute]
    nodes: list[PyCoNode]
    parent: PyFlameObject
    type: str

class PyCoNode:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    type: str

class PyColourMgtTimelineFX:
    attributes: list[PyAttribute]
    has_maps_cache_media: bool
    parent: PyFlameObject
    type: str

class PyCompassNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    nodes: list[PyNode]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyDesktop:
    attributes: list[PyAttribute]
    batch_groups: list[PyBatch]
    children: list[PyFlameObject]
    parent: PyFlameObject
    reel_groups: list[PyReelGroup]
    def create_batch_group(
        arg1: PyDesktop,
        name: str,
        nb_reels: Any = None,
        nb_shelf_reels: Any = None,
        reels: list = None,
        shelf_reels: list = None,
        start_frame: int = 1,
        duration: Any = None,
    ) -> PyBatch: ...
    def create_reel_group(arg1: PyDesktop, name: str) -> PyReelGroup: ...

class PyExporter:
    export_all_subtitles: bool
    export_between_marks: bool
    export_subtitles_as_files: bool
    foreground: bool
    include_subtitles: bool
    keep_timeline_fx_renders: bool
    use_top_video_track: bool
    warn_on_mixed_colour_space: bool
    warn_on_no_media: bool
    warn_on_pending_render: bool
    warn_on_reimport_unsupported: bool
    warn_on_unlinked: bool
    warn_on_unrendered: bool
    BackgroundJobSettings: type[BackgroundJobSettings]
    PresetType: type[PresetType]
    PresetVisibility: type[PresetVisibility]
    def export(
        arg1: PyExporter,
        sources: Any,
        preset_path: str,
        output_directory: str,
        background_job_settings: BackgroundJobSettings | None = None,
        hooks: PythonHookOverride | None = None,
        hooks_user_data: Any = None,
    ) -> None: ...

class PyFlameObject:
    attributes: list[PyAttribute]
    parent: PyFlameObject

class PyFolder:
    attributes: list[PyAttribute]
    batch_groups: list[PyBatch]
    batch_iterations: list[PyBatchIteration]
    children: list[PyFlameObject]
    clips: list[PyClip]
    desktops: list[PyDesktop]
    folders: list[PyFolder]
    parent: PyFlameObject
    reel_groups: list[PyReelGroup]
    reels: list[PyReel]
    sequences: list[PySequence]
    def create_folder(arg1: PyFolder, name: str) -> PyFolder: ...
    def create_reel(arg1: PyFolder, name: str) -> PyReel: ...
    def create_reel_group(arg1: PyFolder, name: str) -> PyReelGroup: ...
    def create_sequence(
        arg1: PyFolder,
        name: str = "Untitled Sequence",
        video_tracks: int = 1,
        video_stereo: bool = False,
        width: Any = None,
        height: Any = None,
        ratio: Any = None,
        bit_depth: Any = None,
        scan_mode: Any = None,
        frame_rate: Any = None,
        start_at: Any = "00:00:00+00",
        duration: Any = "00:00:00+01",
        audio_tracks: int = 1,
        audio_stereo: bool = True,
    ) -> PySequence: ...

class PyGMaskTracerNode:
    attributes: list[PyAttribute]
    cursor_position: tuple[float, float]
    input_sockets: list[str]
    media_layers: list[PyNode]
    node_types: list[str]
    nodes: list[PyNode]
    output_sockets: list[str]
    output_types: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    def create_node(
        arg1: PyActionFamilyNode,
        node_type: str,
        file_path: str = "",
        is_udim: bool = False,
        tile_resolution: int = 0,
        input_colour_space: str = "",
    ) -> PyNode: ...
    def get_node(arg1: PyActionFamilyNode, node_name: str) -> PyNode: ...
    def encompass_nodes(arg1: PyActionFamilyNode, node_list: list) -> PyCoCompass | PyCompassNode: ...

class PyHDRNode:
    analysis_status: str
    attributes: list[PyAttribute]
    input_sockets: list[str]
    mastering_display_ids: list[str]
    mastering_display_info: dict[str, Any]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    target_display_ids: list[str]
    target_display_info: dict[str, Any]

class PyHDRTimelineFX:
    analysis_status: str
    attributes: list[PyAttribute]
    has_maps_cache_media: bool
    mastering_display_ids: list[str]
    mastering_display_info: dict[str, Any]
    parent: PyFlameObject
    target_display_ids: list[str]
    target_display_info: dict[str, Any]
    type: str

class PyImageNode:
    attributes: list[PyAttribute]
    cursor_position: tuple[float, float]
    input_sockets: list[str]
    media_layers: list[PyNode]
    media_nodes: list[PyNode]
    node_types: list[str]
    nodes: list[PyNode]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    def create_node(
        arg1: PyActionFamilyNode,
        node_type: str,
        file_path: str = "",
        is_udim: bool = False,
        tile_resolution: int = 0,
        input_colour_space: str = "",
    ) -> PyNode: ...
    def get_node(arg1: PyActionFamilyNode, node_name: str) -> PyNode: ...
    def encompass_nodes(arg1: PyActionFamilyNode, node_list: list) -> PyCoCompass | PyCompassNode: ...

class PyLensDistortionNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyLibrary:
    attributes: list[PyAttribute]
    batch_groups: list[PyBatch]
    batch_iterations: list[PyBatchIteration]
    children: list[PyFlameObject]
    clips: list[PyClip]
    desktops: list[PyDesktop]
    folders: list[PyFolder]
    opened: bool
    parent: PyFlameObject
    reel_groups: list[PyReelGroup]
    reels: list[PyReel]
    sequences: list[PySequence]
    def create_folder(arg1: PyLibrary, name: str) -> PyFolder: ...
    def create_reel(arg1: PyLibrary, name: str) -> PyReel: ...
    def create_reel_group(arg1: PyLibrary, name: str) -> PyReelGroup: ...
    def create_sequence(
        arg1: PyLibrary,
        name: str = "Untitled Sequence",
        video_tracks: int = 1,
        video_stereo: bool = False,
        width: Any = None,
        height: Any = None,
        ratio: Any = None,
        bit_depth: Any = None,
        scan_mode: Any = None,
        frame_rate: Any = None,
        start_at: Any = "00:00:00+00",
        duration: Any = "00:00:00+01",
        audio_tracks: int = 1,
        audio_stereo: bool = True,
    ) -> PySequence: ...

class PyMarker:
    attributes: list[PyAttribute]
    parent: PyFlameObject

class PyMediaHub:
    archives: PyMediaHubTab
    files: PyMediaHubFilesTab

class PyMediaHubFilesEntry:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    path: str

class PyMediaHubFilesFolder:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    path: str

class PyMediaHubFilesTab:
    options: PyMediaHubFilesTabOptions

class PyMediaHubFilesTabOptions:
    bit_depth: str | None
    cache_and_proxies_all_versions: bool
    cache_mode: str
    frame_ratio: float | None
    height: int | None
    multi_channel_mode: str
    pixel_ratio: float | None
    proxies_mode: str
    resize_filter: str
    resize_mode: str
    resolution: str
    scaling_presets_value: float | None
    scan_mode: str
    sequence_mode: str
    width: int | None

class PyMediaHubProjectsEntry:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    path: str
    uid: str

class PyMediaHubProjectsFolder:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    path: str
    uid: str

class PyMediaPanel:
    dual: bool
    full_height: bool
    full_width: bool
    selected_entries: list[PyFlameObject]
    visible: bool
    def copy(
        arg1: PyMediaPanel, source_entries: Any, destination: Any, duplicate_action: str = "add"
    ) -> list[PyFlameObject]: ...
    def move(
        arg1: PyMediaPanel, source_entries: Any, destination: Any, duplicate_action: str = "add"
    ) -> list[PyFlameObject]: ...

class PyMorphNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyOFXNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyPaintNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyProject:
    attributes: list[PyAttribute]
    current_workspace: PyWorkspace
    description: str
    media_folder: str
    name: str
    nickname: str
    parent: PyFlameObject
    project_folder: str
    project_name: str
    setups_folder: str
    shared_libraries: list[PyLibrary]
    workspaces_count: int
    def create_shared_library(arg1: PyProject, name: str) -> PyLibrary: ...

class PyProjectSelector:
    current_project: PyProject

class PyReel:
    attributes: list[PyAttribute]
    children: list[PyFlameObject]
    clips: list[PyClip]
    parent: PyFlameObject
    sequences: list[PySequence]
    type: str
    def create_sequence(
        arg1: PyReel,
        name: str = "Untitled Sequence",
        video_tracks: int = 1,
        video_stereo: bool = False,
        width: Any = None,
        height: Any = None,
        ratio: Any = None,
        bit_depth: Any = None,
        scan_mode: Any = None,
        frame_rate: Any = None,
        start_at: Any = "00:00:00+00",
        duration: Any = "00:00:00+01",
        audio_tracks: int = 1,
        audio_stereo: bool = True,
    ) -> PySequence: ...

class PyReelGroup:
    attributes: list[PyAttribute]
    children: list[PyFlameObject]
    parent: PyFlameObject
    reels: list[PyReel]
    def create_reel(arg1: PyReelGroup, name: str, sequence: bool = False) -> PyReel: ...

class PyRenderNode:
    attributes: list[PyAttribute]
    channels: list[tuple[str, str]]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyResolution:
    bit_depth: str
    frame_ratio: float | None
    height: int | None
    resolution: str
    scan_mode: str
    width: int | None

class PySearch:
    use_weight: bool

class PySegment:
    attributes: list[PyAttribute]
    container_clip: PyClip
    effect_types: list[str]
    effects: list[PyTimelineFX]
    file_path: str
    groups: list[PySequenceGroup]
    head: PyTime
    markers: list[PyMarker]
    matte_channel: str
    matte_channels: list[str]
    matte_mode: str
    original_source_uid: str
    parent: PyFlameObject
    record_duration: PyTime
    record_in: PyTime
    record_out: PyTime
    rgb_channel: str
    rgb_channels: list[str]
    source_audio_track: int
    source_bit_depth: str
    source_cached: bool
    source_colour_primaries: str
    source_duration: PyTime
    source_essence_uid: str
    source_frame_rate: str
    source_has_history: bool
    source_height: int
    source_in: PyTime
    source_matrix_coefficients: str
    source_name: str
    source_out: PyTime
    source_ratio: float
    source_sample_rate: str
    source_scan_mode: str
    source_transfer_characteristics: str
    source_uid: str
    source_unlinked: bool
    source_width: int
    start_frame: int
    tail: PyTime
    tape_name: str
    type: str
    version_uid: str
    version_uids: list[str]
    def create_effect(arg1: PySegment, effect_type: str, after_effect_type: str = "") -> PyTimelineFX: ...
    def create_marker(arg1: PySegment, location: Any) -> PyMarker: ...
    def connected_segments(arg1: PySegment, scoping: str = "all reels") -> list[PySegment]: ...
    def shared_source_segments(arg1: PySegment) -> list[PySegment]: ...
    def copy_to_media_panel(arg1: PySegment, destination: PyArchiveEntry, duplicate_action: str = "add") -> PyClip: ...

class PySequence:
    archive_date: str
    archive_error: str
    attributes: list[PyAttribute]
    audio_tracks: list[PyAudioTrack]
    bit_depth: str
    cached: bool
    colour_primaries: str
    creation_date: str
    duration: PyTime
    essence_uid: str
    frame_rate: str
    groups: list[PySequenceGroup]
    has_deliverables: bool
    has_history: bool
    height: int
    markers: list[PyMarker]
    matrix_coefficients: str
    original_source_uid: str
    parent: PyFlameObject
    proxy_resolution: str
    ratio: float
    sample_rate: str
    scan_mode: str
    source_uid: str
    start_frame: int
    subtitles: list[PySubtitleTrack]
    transfer_characteristics: str
    unlinked: bool
    versions: list[PyVersion]
    width: int
    def create_audio(arg1: PySequence, stereo: bool = False) -> PyAudioTrack: ...
    def create_group(arg1: PySequence, name: str) -> PySequenceGroup: ...
    def create_marker(arg1: PyClip, location: Any) -> PyMarker: ...
    def create_subtitle(arg1: PySequence) -> PySubtitleTrack: ...
    def create_version(arg1: PySequence, stereo: bool = False) -> PyVersion: ...
    def create_container(arg1: PySequence) -> PyClip: ...
    def open_as_sequence(arg1: PyClip) -> PySequence: ...

class PySequenceGroup:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    segments: list[PySegment]

class PySubtitleTrack:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    segments: list[PySegment]
    transitions: list[PyTransition]
    def insert_transition(
        arg1: PyTrack,
        record_time: PyTime,
        type: str,
        duration: int = 10,
        alignment: str = "Centred",
        in_offset: int = 0,
        sync: bool = False,
    ) -> PyTransition: ...
    def copy_to_media_panel(arg1: PyTrack, destination: PyArchiveEntry, duplicate_action: str = "add") -> PyClip: ...

class PyTime:
    frame: int
    frame_rate: str
    relative_frame: int
    timecode: str

class PyTimeline:
    clip: PyClip | PySequence | None
    current_effect: PyTimelineFX | None
    current_marker: PyMarker | None
    current_segment: PySegment | None
    current_transition: PyTransition | None
    type: str

class PyTimelineFX:
    attributes: list[PyAttribute]
    has_maps_cache_media: bool
    parent: PyFlameObject
    type: str

class PyTimewarpNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]

class PyTimewarpTimelineFX:
    attributes: list[PyAttribute]
    has_maps_cache_media: bool
    parent: PyFlameObject
    type: str

class PyTrack:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    segments: list[PySegment]
    transitions: list[PyTransition]
    def insert_transition(
        arg1: PyTrack,
        record_time: PyTime,
        type: str,
        duration: int = 10,
        alignment: str = "Centred",
        in_offset: int = 0,
        sync: bool = False,
    ) -> PyTransition: ...
    def copy_to_media_panel(arg1: PyTrack, destination: PyArchiveEntry, duplicate_action: str = "add") -> PyClip: ...

class PyTransition:
    attributes: list[PyAttribute]
    in_offset: int
    parent: PyFlameObject
    record_time: PyTime
    type: str

class PyTypeFX:
    attributes: list[PyAttribute]
    has_maps_cache_media: bool
    layers: list[PyTypeLayer]
    parent: PyFlameObject
    type: str
    def add_layer(arg1: PyTypeFX, layer_type: str = "Centre") -> PyTypeLayer: ...

class PyTypeLayer:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    type: str

class PyTypeNode:
    attributes: list[PyAttribute]
    input_sockets: list[str]
    layers: list[PyTypeLayer]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    def add_layer(arg1: PyTypeNode, layer_type: str = "Centre") -> PyTypeLayer: ...

class PyUser:
    name: str
    nickname: str
    shortcuts_profile: str

class PyUsers:
    current_user: PyUser

class PyVersion:
    attributes: list[PyAttribute]
    parent: PyFlameObject
    stereo: bool
    tracks: list[PyTrack]
    def create_track(arg1: PyVersion, track_index: int = -1, hdr: bool = False) -> PyTrack: ...
    def copy_to_media_panel(arg1: PyVersion, destination: PyArchiveEntry, duplicate_action: str = "add") -> PyClip: ...

class PyWorkspace:
    attributes: list[PyAttribute]
    desktop: PyDesktop
    libraries: list[PyLibrary]
    parent: PyFlameObject
    def create_library(arg1: PyWorkspace, name: str) -> PyLibrary: ...

class PyWriteFileNode:
    attributes: list[PyAttribute]
    channels: list[tuple[str, str]]
    input_sockets: list[str]
    output_sockets: list[str]
    parent: PyFlameObject
    sockets: dict[str, Any]
    def get_resolved_media_path(
        arg1: PyWriteFileNode, show_extension: bool = True, translate_path: bool = True, frame: Any = None
    ) -> str: ...
