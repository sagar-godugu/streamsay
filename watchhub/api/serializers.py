from rest_framework import serializers
from watchhub.models import StreamPlatform,WatchContent,ContentReview

class ContentReviewSerializer(serializers.ModelSerializer):
    critic=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=ContentReview
        # fields="__all__"
        exclude=['watchcontent']

class WatchContentSerializer(serializers.ModelSerializer):
    reviewcontent=ContentReviewSerializer(many=True,read_only=True)
    class Meta:
        model=WatchContent
        fields="__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):         
    watchcontent=WatchContentSerializer(many=True,read_only=True)   # nested serializers
    class Meta:                                                     # WatchConetentSerializer inside the
        model=StreamPlatform                                        # StreamPlatformSerializer to do that
        fields='__all__'                                            # we need to write related_name="any"
                                                                    # while creating the watchcontent model




#----------------------Validations----------------------#
    # title_length=serializers.SerializerMethodField()
    # def get_title_length(self,object):
    #     return len(object.title)

    # def name_length(value):
    #     if len(value)<2:
    #         raise serializers.ValidationError("More than two letters")
    # def validate(self, data):
    #     if data['title']==data['desc']:
    #         raise serializers.ValidationError("title and desc should be different")

#-----------------Using Normal Serializer class-----------------#
    # class WatchContentSerializer(serializers.Serializer):
    #     id = serializers.PrimaryKeyRelatedField(read_only = True)
    #     title=serializers.CharField(validators=[name_length])
    #     desc=serializers.CharField()
    #     isAvailable=serializers.BooleanField()

    #     def create(self, validated_data):
    #         return WatchContent.objects.create(**validated_data)


#---------------------------------------------------#
    # watchcontent=serializers.StringRelatedField(many=True)
    # watchcontent=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # watchcontent=serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watch-content-individual',
    #  )

    # watchcontentlist=WatchContentSerializer(many=True,read_only=True)