from enum import Enum


class EventCodeEnum(str, Enum):
    MANUAL_CANCEL_SERVICE_TICKET = "manual_cancel_service_ticket"
    MANUAL_TRACING_START_SERVICE_TICKET = "manual_tracing_start_service_ticket"
    MANUAL_TRACING_STOP_SERVICE_TICKET = "manual_tracing_stop_service_ticket"
    MANUAL_CREATE_SERVICE_TICKET = "manual_create_service_ticket"
    MANUAL_IMPORT_RESERVATION_SMWS = "manual_import_reservation_smws"
    MANUAL_MODIFY_USER_SERVICE_TICKET = "manual_modify_user_service_ticket"
    MANUAL_MODIFY_ESTIMATED_ARRIVAL_TIME_SERVICE_TICKET = "manual_modify_estimated_arrival_time_service_ticket"
    MANUAL_MODIFY_ESTIMATED_DELIVERY_TIME_SERVICE_TICKET = "manual_modify_estimated_delivery_time_service_ticket"
    MANUAL_DELETE_ESTIMATED_DELIVERY_TIME_SERVICE_TICKET = "manual_delete_estimated_delivery_time_service_ticket"
    MANUAL_BOOKING_MESSAGE_SERVICE_TICKET = "manual_booking_message_service_ticket"
    MANUAL_DELIVERY_MESSAGE_SERVICE_TICKET = "manual_delivery_message_service_ticket"

    SYSTEM_TRACING_START_SERVICE_TICKET = "system_tracing_start_service_ticket"
    SYSTEM_TRACING_STOP_SERVICE_TICKET = "system_tracing_stop_service_ticket"

    NOSHOW_SERVICE_TICKET_AUTO_CANCEL = "noshow_service_ticket_auto_cancel"
    IMPORT_RESERVATION_CONFLICT_AUTO_CANCEL = "import_reservation_conflict_auto_cancel"
    BOOKING_REMINDING_SERVICE_TICKET = "booking_reminding_service_ticket"
    TODAY_REPAIR_WORKING_SERVICE_TICKET_AUTO_CLOSED = "today_repair_working_service_ticket_auto_closed"

    CAR_IN_ESTABLISHED = "car_in_established"
    CAR_IN_RECEPTION = "car_in_reception"
    CAR_IN_WORKING = "car_in_working"
    CAR_IN_DISPATCH = "car_in_dispatch"
    CAR_IN_DETAILING = "car_in_detailing"
    CAR_IN_NO_TICKET = "car_in_no_ticket"
    CAR_OUT_FINISHED = "car_out_finished"
    CAR_OUT_GENERAL = "car_out_general"
    CAR_OUT_NO_SERVE = "car_out_no_serve"
    CAR_OUT_TEST = "car_out_test"
    CAR_OUT_ACC = "car_out_acc"

    LPR_CHANGE_STATE = "lpr_change_state"
    LPR_CHANGE_POSITION = "lpr_change_position"

    REPAIR_OVERDUE = "repair_overdue"
    DETAILING_OVERDUE = "detailing_overdue"
