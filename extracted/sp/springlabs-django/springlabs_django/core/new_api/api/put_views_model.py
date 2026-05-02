# START API API_NAMEViewSetPut (Created by SPRINGLABS_DJANGO)
class API_NAMEViewSetPut(mixins.UpdateModelMixin, viewsets.GenericViewSet):
	model = User
	queryset = User.objects.all()
	serializer_class = API_NAMESerializerPut

	def update(self, request, *args, **kwargs):
		"""
			Descripción de método update en documentación
		"""
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		response=response_maker_1("Message",serializer.data,status.HTTP_200_OK)
		return Response(response)

API_NAMEPut = API_NAMEViewSetPut.as_view(
	name="API_NAME",
	description="Descripción de API_NAME",
	actions={
		'put': 'update'
	}
)
# END API API_NAMEViewSetPut (Created by SPRINGLABS_DJANGO)