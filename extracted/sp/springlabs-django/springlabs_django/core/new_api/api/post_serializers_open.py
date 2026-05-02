# START API API_NAMESerializerPost (Created by SPRINGLABS_DJANGO)
class API_NAMESerializerPost(serializers.Serializer):
    field = serializers.CharField(label="Username",
        help_text="A unique string value identifying User",
        required=True,
        max_length=100)

    def validate_field(self, value):
        """
            Breve descripción de método que valida campo field.

            Descripción detallada de método que valida campo field, esta
            descripción detallada puede llevar varias lineas.
            Parámetros:
                param           [Type]         Descripción de param
            Excepciones:
                Excepcion       [Type]         Descripción de excepción
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

    def create(self, validated_data):
        """
            Breve descripción de método create.

            Descripción detallada de método create, esta
            descripción detallada puede llevar varias lineas.
            Parámetros:
                param           [Type]          Descripción de param
            Excepciones:
                Excepcion       [Type]          Descripción de excepción
            Retorno:
                retorno        [Type]          Descripción de retorno
        """
        return validated_data
# END API API_NAMESerializerPost (Created by SPRINGLABS_DJANGO)
