APP_NAME_TO_USECASE = {
    "people_counting": "people_counting",
    "mask_detection": "mask_detection",
    "vehicle_monitoring": "vehicle_monitoring",
    "vehicle_type_monitoring": "vehicle_monitoring",
    "weapon_detection": "weapon_detection",
    "traffic_sign_monitoring": "traffic_sign_monitoring",
    "flare_analysis": "flare_analysis",
    "ppe_compliance": "ppe_compliance",
    "advanced_customer_service": "advanced_customer_service",
    "assembly_line_detection": "assembly_line_detection",
    "crop_weed_detection"  : "crop_weed_detection",
    "emergency_vehicle_detection": "emergency_vehicle_detection",
    "fashion_detection": "fashion_detection",
    "gender_detection": "gender_detection",
    "price_tag_detection": "price_tag_detection",
    "windmill_maintenance": "windmill_maintenance",
    "underwater_pollution_detection": "underwater_pollution_detection",
    "solar_panel": "solar_panel",
    "face_emotion": "face_emotion",
    "pedestrian_detection": "pedestrian_detection",
    "warehouse_object_segmentation": "warehouse_object_segmentation",
    "flower_segmentation": "flower_segmentation",
    "shopping_cart_analysis": "shopping_cart_analysis",
    "car_part_segmentation": "car_part_segmentation",
}

APP_NAME_TO_CATEGORY = {
    "people_counting": "general",
    "mask_detection": "mask_detection",
    "vehicle_monitoring": "traffic",
    "vehicle_type_monitoring": "traffic",
    "weapon_detection": "security",
    "traffic_sign_monitoring": "traffic",
    "flare_analysis": "flare_detection",
    "ppe_compliance": "security",
    "advanced_customer_service": "sales",
    "assembly_line_detection": "manufacturing",
    "crop_weed_detection": "agriculture",
    "emergency_vehicle_detection": "traffic",
    "fashion_detection": "retail",
    "gender_detection": "general",
    "price_tag_detection": "retail",
    "windmill_maintenance": "windmill_maintenance",
    "underwater_pollution_detection": "environmental",
    "solar_panel": "energy",
    "face_emotion": "general",
    "pedestrian_detection": "pedestrian",
    "warehouse_object_segmentation": "retail",
    "flower_segmentation": "agriculture",
    "shopping_cart_analysis": "retail",
    "car_part_segmentation": "automobile"
}

def get_usecase_from_app_name(app_name: str) -> str:
    normalized_app_name = app_name.lower().replace(" ", "_").replace("-", "_")
    return APP_NAME_TO_USECASE.get(app_name, APP_NAME_TO_USECASE.get(normalized_app_name))

def get_category_from_app_name(app_name: str) -> str:
    normalized_app_name = app_name.lower().replace(" ", "_").replace("-", "_")
    return APP_NAME_TO_CATEGORY.get(app_name, APP_NAME_TO_CATEGORY.get(normalized_app_name))
