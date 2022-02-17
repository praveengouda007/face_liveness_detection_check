
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import UploadSerializer
# from face_liveness_detection.face_anti_spoofing import Liveness_Api
from face_liveness_detection import liveness_detection
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from rest_framework.views import APIView

# ViewSets define the view behavior.
fs = FileSystemStorage(location='file/')
class UploadView(APIView):
    # serializer_class = UploadSerializer

    def list(self, request):
        return Response("Get Video")

    def post(self, request):
        # import pdb; pdb.set_trace()
        # file_uploaded = request.FILES.get('video')
        file = request.FILES["video"]
        content = file.read()
        file_content = ContentFile(content)
        file_name = fs.save(
            "video.mp4", file_content
        )
        video = fs.path(file_name)
        output = liveness_detection.checking_liveness(video,selfie_name='')
        return Response(output)
