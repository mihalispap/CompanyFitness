from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
import cv2

# Create your views here.
from pytesseract import pytesseract
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from app import utils
from app import api_models


@api_view(('GET',))
def identify_fitness_metric(request):
    if not request.query_params.get('image_path'):
        raise APIException(code=status.HTTP_400_BAD_REQUEST)
    img = cv2.imread(request.query_params.get('image_path'))
    res = pytesseract.image_to_string(img, config="--psm 6")

    extractor = utils.ImageExtractor(image_str=res)
    identified = []
    identified.append(api_models.ImageIdentification(
        metric='steps',
        value=extractor.steps,
        tracked_on=extractor.tracked_on,
    ).dict())

    return Response(identified, status=status.HTTP_200_OK)
