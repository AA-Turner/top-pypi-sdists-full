from __future__ import print_function
import traceback
import sys
import os


class SwimlaneException(Exception):
    TB_ERROR_STREAM = sys.stderr  # Change me if you wish to redirect the tracdeback error stream

    @staticmethod
    def disable_tb_stream():
        SwimlaneException.TB_ERROR_STREAM = open(os.devnull, 'w')
    
    @staticmethod
    def reset_tb_stream():
        if not SwimlaneException.TB_ERROR_STREAM.closed:
            SwimlaneException.TB_ERROR_STREAM.close()

        SwimlaneException.TB_ERROR_STREAM = sys.stderr

    """Generic Swimlane Exception Baseclass"""
    def __init__(self, message=None, *args):
        if not message:
            message = "Unknown SwimlaneException"

        custom_message = self.get_custom_message(*args)

        if custom_message:
            custom_message = "{} - ".format(custom_message)
        else:
            cls_name = self.__class__.__name__
            custom_message = "{} - ".format(cls_name)

        message = "{cust_msg}{msg}".format(cust_msg=custom_message, msg=message)

        super(SwimlaneException, self).__init__(message)  # Call super with formatted message data

        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_tb is not None:  # Check if we're in a nested traceback situation
            print("Exception", file=SwimlaneException.TB_ERROR_STREAM)
            traceback.print_exc(file=SwimlaneException.TB_ERROR_STREAM)
            print("Raised at:", file=SwimlaneException.TB_ERROR_STREAM)

    def get_custom_message(self, args):
        raise NotImplementedError


class SwimlaneIntegrationException(SwimlaneException):
    """Thrown when an Exception in a Swimlane task is expected"""
    def get_custom_message(self, *args):
        return None


class SwimlaneIntegrationAuthException(SwimlaneIntegrationException):
    """Thrown when an Exception in a Swimlane auth task is expected"""
    def get_custom_message(self, *args):
        return None


class InvalidInput(SwimlaneException):
    def __init__(self, message, input_name, input_value):
        super(InvalidInput, self).__init__(message, input_name, input_value)
        self.input_name = input_name
        self.input_value = input_value

    def get_custom_message(self, *args):
        # args[0] -> first __init__ arg (minus message) -> input_name
        # args[1] - > second __init__ arg -> input_value
        return "Invalid Input for field '{}' on value '{}'".format(args[0], args[1])


class ConnectionError(SwimlaneException):
    def __init__(self, message, host, port=80, protocol="https"):
        super(ConnectionError, self).__init__(message, host, port, protocol)
        self.host = host
        self.port = port
        self.protocol = protocol

    def get_custom_message(self, *args):
        return "Connection Failed at Host: '{}', On port: '{}', Using protocol '{}'".format(args[0], args[1], args[2])


class InvalidCredentials(SwimlaneException):
    def __init__(self, message):
        super(InvalidCredentials, self).__init__(message)

    def get_custom_message(self, *args):
        return "Invalid Credentials"


class ResourceNotFound(SwimlaneException):
    def __init__(self, message, resource_name):
        super(ResourceNotFound, self).__init__(message, resource_name)
        self.resource_name = resource_name

    def get_custom_message(self, *args):
        return "Resource Not Found '{}'".format(args[0])
