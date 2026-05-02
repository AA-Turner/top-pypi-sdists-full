# START API API_NAMESerializerPut (Created by SPRINGLABS_DJANGO)
class API_NAMESerializerPut(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)

    def validate_email(self, value):
        """
            Breve descripción de método que valida campo email.

            Descripción detallada de método que valida campo email, esta
            descripción detallada puede llevar varias lineas.
            Parámetros:
                param           [Type]          Descripción de param
            Excepciones:
                Excepcion       [Type]          Descripción de excepción
            Retorno:
                retorno        [Type]          Descripción de retorno
        """
        return value

    def validate(self, validated_data):
        """
            Breve descripción de método validate.

            Descripción detallada de método validate, esta
            descripción detallada puede llevar varias lineas.
            Parámetros:
                param           [Type]          Descripción de param
            Excepciones:
                Excepcion       [Type]          Descripción de excepción
            Retorno:
                retorno        [Type]          Descripción de retorno
        """
        return validated_data

    def update(self, instance, validated_data):
        """
            Breve descripción de método update.

            Descripción detallada de método update, esta
            descripción detallada puede llevar varias lineas.
            Parámetros:
                param           [Type]          Descripción de param
            Excepciones:
                Excepcion       [Type]          Descripción de excepción
            Retorno:
                retorno        [Type]          Descripción de retorno
        """
        return validated_data
# END API API_NAMESerializerPut (Created by SPRINGLABS_DJANGO)
