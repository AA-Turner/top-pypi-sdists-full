# START API API_NAMEViewSetDelete (Created by SPRINGLABS_DJANGO)
class API_NAMEViewSetDelete(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = API_NAMESerializerDelete

    def destroy(self, request, *args, **kwargs):
        """
            Descripción de método destroy en documentación
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.destroy(instance, serializer.validated_data)
        response = response_maker_1(
            "Message", serializer.data, status.HTTP_200_OK)
        return Response(response)

API_NAMEDelete = API_NAMEViewSetDelete.as_view(
    name="API_NAME",
    description="Descripción de API_NAME",
    actions={
        'delete': 'destroy'
    }
)
# END API API_NAMEViewSetDelete (Created by SPRINGLABS_DJANGO)