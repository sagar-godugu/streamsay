from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from user_auth.api.serializers import RegisterSerializer

@api_view(['POST',])
def register_view(request):
    if request.method=='POST':
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"User registered successfully.."},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        

#----------------Used when dealing with TokenAuthentication-----------------#
    # @api_view(['POST',])
    # def logout_view(request):
    #     if request.method=='POST':
    #         request.user.auth_token.delete()
    #         return Response({'message':'User Logged Out successfully'},status=status.HTTP_200_OK)
        
