# presentation/serializers.py
from rest_framework import serializers

class StudentCourseItemSerializer(serializers.Serializer):
    student_name = serializers.CharField(max_length=255)
    student_doc = serializers.CharField(max_length=50)
    student_signature = serializers.URLField(required=False, allow_null=True)
    
    instructor_name = serializers.CharField(max_length=255)
    instructor_doc = serializers.CharField(max_length=50)
    instructor_signature = serializers.URLField(required=False, allow_null=True)
    
    course_name = serializers.CharField(max_length=255)
    duration = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class CourseBatchProcessSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=StudentCourseItemSerializer(),
        allow_empty=False
    )