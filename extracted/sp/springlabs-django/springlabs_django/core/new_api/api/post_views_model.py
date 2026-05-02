# START API API_NAMEViewSetPost (Created by SPRINGLABS_DJANGO)
class API_NAMEViewSetPost(mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = User
    queryset = User.objects.all()
    serializer_class = API_NAMESerializerPost
    
    def create(self, request, *args, **kwargs):
        """
            Descripción de método create en documentación
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = response_maker_1(
            "Message", serializer.data, status.HTTP_200_OK)
        return Response(response)

API_NAMEPost = API_NAMEViewSetPost.as_view(
    name="API_NAME",
    description="Descripción de API_NAME",
    actions={
        'post': 'create'
    }
)
# END API API_NAMEViewSetPost (Created by SPRINGLABS_DJANGO)