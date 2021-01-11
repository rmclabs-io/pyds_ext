#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "nvdsmeta.h"
#include <iostream>
#include "nvll_osd_struct.h"
using namespace std;
namespace py = pybind11;

PYBIND11_MODULE(pyds_bbox_meta, m) {
    m.doc() = "pybind11 wrapper to access Nvidia DeepStream detector bbox";

#define STRING_CHAR_ARRAY(TYPE, FIELD)                             \
        [](const TYPE &self)->string {                             \
            return string(self.FIELD);                             \
        },                                                         \
        [](TYPE &self, std::string str) {                          \
            int strSize = str.size();                              \
            str.copy(self.FIELD, strSize);                         \
        },                                                         \
        py::return_value_policy::reference

	py::class_<NvDsObjectMeta>(m,"NvDsObjectMeta",py::module_local())
                .def(py::init<>())
                .def_readwrite("base_meta", &NvDsObjectMeta::base_meta)
       
                .def_readwrite("parent", &NvDsObjectMeta::parent)
        
                .def_readwrite("unique_component_id", &NvDsObjectMeta::unique_component_id)
       
                .def_readwrite("class_id", &NvDsObjectMeta::class_id)        
        
                .def_readwrite("object_id", &NvDsObjectMeta::object_id)
        
                .def_readwrite("detector_bbox_info",&NvDsObjectMeta::detector_bbox_info)

                .def_readwrite("tracker_bbox_info",&NvDsObjectMeta::tracker_bbox_info) 
            
                .def_readwrite("confidence", &NvDsObjectMeta::confidence)

                .def_readwrite("tracker_confidence",&NvDsObjectMeta::tracker_confidence)
        
                .def_readwrite("rect_params", &NvDsObjectMeta::rect_params)

                .def_readwrite("mask_params",&NvDsObjectMeta::mask_params)
	
                .def_readwrite("text_params", &NvDsObjectMeta::text_params)
                
                .def("cast",[](void *data) {
                        return (NvDsObjectMeta*)data;},
                        py::return_value_policy::reference)
        
                .def_property("obj_label", STRING_CHAR_ARRAY(NvDsObjectMeta, obj_label))
                .def_readwrite("classifier_meta_list", &NvDsObjectMeta::classifier_meta_list)        
     
                .def_readwrite("obj_user_meta_list", &NvDsObjectMeta::obj_user_meta_list)
                .def_property("misc_obj_info",
				[](NvDsObjectMeta &self)->py::array {
					auto dtype=py::dtype(py::format_descriptor<int>::format());
                    auto base=py::array(dtype, {MAX_USER_FIELDS}, {sizeof(int)});
                    return py::array(dtype,{MAX_USER_FIELDS}, {sizeof(int)}, self.misc_obj_info,base);
				}, [](NvDsObjectMeta& self){})
                .def_property("reserved",
				[](NvDsObjectMeta &self)->py::array {
					auto dtype=py::dtype(py::format_descriptor<int>::format());
                    auto base=py::array(dtype, {MAX_RESERVED_FIELDS}, {sizeof(int)});
                    return py::array(dtype,{MAX_RESERVED_FIELDS}, {sizeof(int)}, self.reserved,base);
				}, [](NvDsObjectMeta& self){});

	py::class_<NvOSD_RectParams>(m,"NvOSD_RectParams",py::module_local())
                .def(py::init<>())
                .def_readwrite("left",&NvOSD_RectParams::left)
                .def_readwrite("top",&NvOSD_RectParams::top)
                .def_readwrite("width",&NvOSD_RectParams::width)
                .def_readwrite("height",&NvOSD_RectParams::height)
                .def_readwrite("border_width",&NvOSD_RectParams::border_width)
                .def_readwrite("border_color",&NvOSD_RectParams::border_color)
                .def_readwrite("has_bg_color",&NvOSD_RectParams::has_bg_color)
                .def_readwrite("reserved",&NvOSD_RectParams::reserved)
                .def_readwrite("bg_color",&NvOSD_RectParams::bg_color)
                .def_readwrite("has_color_info",&NvOSD_RectParams::has_color_info)
                .def_readwrite("color_id",&NvOSD_RectParams::color_id);
	py::class_<NvDsComp_BboxInfo>(m,"NvDsComp_BboxInfo",py::module_local())
                .def(py::init<>())

                .def_readwrite("org_bbox_coords",&NvDsComp_BboxInfo::org_bbox_coords);

	 py::class_<NvBbox_Coords>(m,"NvBbox_Coords",py::module_local())
            .def(py::init<>())
            .def_readwrite("left",&NvBbox_Coords::left)
            .def_readwrite("top",&NvBbox_Coords::top)
            .def_readwrite("width",&NvBbox_Coords::width)
            .def_readwrite("height",&NvBbox_Coords::height);
}