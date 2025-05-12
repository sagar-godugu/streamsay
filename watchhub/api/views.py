from . serializers import StreamPlatformSerializer,WatchContentSerializer,ContentReviewSerializer
from rest_framework.views import APIView
from watchhub.models import StreamPlatform,WatchContent,ContentReview
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from watchhub.api.permissions import IsAdminOrReadOnly,IsCriticOrReadOnly
from rest_framework import viewsets

#----------------- ---StreamPlatoform using ViewSets -----------------------#
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]
    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializer

#------------------------WatchContent----------------------------------------#

class WatchContentListAV(APIView):                          # WatchContent API Views are created using
    permission_classes=[IsAdminOrReadOnly]                        # class based views by inheriting the APIView 
    def get(self,request):                                  # class, it used for more modifications
        content=WatchContent.objects.all()
        stream_data=WatchContentSerializer(content,many=True)
        return Response(stream_data.data)
    
    def post(self,request):
        data=request.data
        serializer=WatchContentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)
        

class WatchContentIndividualAV(APIView):
    permission_classes=[IsAdminOrReadOnly]

    def get(self,request,pk):
        instancedata=get_object_or_404(WatchContent,pk=pk)
        stream_data=WatchContentSerializer(instancedata)
        return Response(stream_data.data)
    
    def put(self,request,pk):
        data=request.data
        instancedata=get_object_or_404(WatchContent,pk=pk)
        stream_data=WatchContentSerializer(instancedata,data)
        if stream_data.is_valid():
            stream_data.save()
            return Response(stream_data.data,status=status.HTTP_200_OK)
        else:
            return Response(stream_data.errors,status=status.HTTP_403_FORBIDDEN)
        
    def patch(self,request,pk):
        data=request.data
        instancedata=get_object_or_404(WatchContent,pk=pk)
        stream_data=WatchContentSerializer(instancedata,data,partial=True)
        if stream_data.is_valid():
            stream_data.save()
            return Response(stream_data.data,status=status.HTTP_200_OK)
        else:
            return Response(stream_data.errors,status=status.HTTP_403_FORBIDDEN)
        
    def delete(self,request,pk):
        instancedata=get_object_or_404(WatchContent,pk=pk)
        instancedata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#----------------------------Content Review ---------------------------------#

class ContentReviewListGv(generics.ListAPIView):       # ContentReview ApiViews are created using Concrete
    permission_classes=[IsCriticOrReadOnly]               # APIViews (generics)
    serializer_class=ContentReviewSerializer           # queryset=ContentReview.objects.all()
    def get_queryset(self):                            # get_queryset() is used to override the queryset. 
        pk=self.kwargs['pk']
        return ContentReview.objects.filter(watchcontent=pk)

class ContentReviewCreateGv(generics.CreateAPIView):
    permission_classes=[IsCriticOrReadOnly]
    serializer_class=ContentReviewSerializer
    def get_queryset(self):                                           
        return ContentReview.objects.all()             
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchcontent=WatchContent.objects.get(pk=pk)
        critic=self.request.user
        review_queryset=ContentReview.objects.filter(watchcontent=watchcontent,critic=critic)

        if review_queryset:
            raise ValidationError("You have already given review..")
        if watchcontent.total_rating==0:
            watchcontent.avg_rating=serializer.validated_data['rating']
        else:
            watchcontent.avg_rating=(watchcontent.avg_rating+serializer.validated_data['rating'])/2

        watchcontent.total_rating+=1
        watchcontent.save()
        serializer.save(watchcontent=watchcontent,critic=critic)
        
class ContentReviewIndividualGv(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsCriticOrReadOnly|IsAdminOrReadOnly]
    queryset=ContentReview.objects.all()
    serializer_class=ContentReviewSerializer

        
        
#---------------Using Function Based Views--------------#
    # @api_view(['GET'])
    # def streamView(request):
    #     if request.method=='GET':
    #         plat_data=StreamPlatform.objects.all()
    #         streamdata=StreamPlatformSerializer(plat_data,many=True)
            
    #         return Response(streamdata.data)



#-------------------- Using Mixins---------------------#
    # from rest_framework import mixins

    # class ContentReviewListMV(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):  
    #     queryset=ContentReview.objects.all()
    #     serializer=ContentReviewSerializer
    #     def get(self,request,*args,**kwargs):
    #         return self.list(request,*args,**kwargs)  
    #     def post(self,request,*args,**kwargs):
    #         return self.create(request,*args,**kwargs)
        
    # class ContentReviewIndividualMV(mixins.RetrieveModelMixin,generics.GenericAPIView):  
    #     queryset=ContentReview.objects.all()
    #     serializer=ContentReviewSerializer
    #     def get(self,request,*args,**kwargs):
    #         return self.retrieve(request,*args,**kwargs)


#----------------- StreamPlatoform using APIView Class-----------------------#

    # class StreamPlatformListAV(APIView):
    #     permission_classes=[IsAdminUser]
    #     def get(self,request):
    #         platform_data=StreamPlatform.objects.all()
    #         stream_data=StreamPlatformSerializer(platform_data,many=True,context={'request':request})
    #         print(stream_data.data)
    #         return Response(stream_data.data)
        
    #     def post(self,request):
    #         data=request.data
    #         stream_data=StreamPlatformSerializer(data)
    #         if stream_data.is_valid():
    #             stream_data.save()
    #             return Response(stream_data.data,status=status.HTTP_200_OK)
    #         else:
    #             return Response(stream_data.errors,status=status.HTTP_403_FORBIDDEN)
            
    # class StreamPlatformIndividualAV(APIView):
    #     permission_classes=[IsAdminUser]
    #     def get(self,request,pk):
    #         data=StreamPlatform.objects.get(pk=pk)
    #         stream_data=StreamPlatformSerializer(data,context={'request':request})
    #         return Response(stream_data.data)
        
    #     def put(self,request,pk):
    #         data=request.data
    #         instancedata=get_object_or_404(StreamPlatform,pk=pk)
    #         stream_data=StreamPlatformSerializer(instancedata,data)
    #         if stream_data.is_valid():
    #             stream_data.save()
    #             return Response(stream_data.data,status=status.HTTP_200_OK)
    #         else:
    #             return Response(stream_data.errors,status=status.HTTP_403_FORBIDDEN)
            
    #     def patch(self,request,pk):
    #         data=request.data
    #         instancedata=get_object_or_404(StreamPlatform,pk=pk)
    #         stream_data=StreamPlatformSerializer(instancedata,data,partial=True)
    #         if stream_data.is_valid():
    #             stream_data.save()
    #             return Response(stream_data.data,status=status.HTTP_200_OK)
    #         else:
    #             return Response(stream_data.errors,status=status.HTTP_403_FORBIDDEN)
            
    #     def delete(self,request,pk):
    #         instancedata=get_object_or_404(StreamPlatform,pk=pk)
    #         instancedata.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
        
#from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser