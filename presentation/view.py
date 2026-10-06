# presentation/views.py
import zipfile
from io import BytesIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CourseBatchProcessSerializer
from infrastructure.pdf.generator import PDFReportService

class GeneratePDFsView(APIView):
    def post(self, request):
        serializer = CourseBatchProcessSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data_list = serializer.validated_data['items']
        
        # 1. Gerar o PDF com a lista consolidada
        list_pdf = PDFReportService.generate_students_list(data_list)
        
        # 2. Criar um arquivo ZIP contendo o PDF da lista + PDFs individuais dos alunos
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            # Salva a lista geral
            zip_file.writestr("Lista_Geral_Alunos.pdf", list_pdf.getvalue())
            
            # Salva os certificados individuais
            for idx, student in enumerate(data_list):
                ind_pdf = PDFReportService.generate_individual_certificate(student)
                file_name = f"Certificado_{student['student_doc']}_{idx+1}.pdf"
                zip_file.writestr(file_name, ind_pdf.getvalue())
        
        zip_buffer.seek(0)
        
        # Retorna o arquivo ZIP contendo todos os PDFs gerados
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="certificados_e_lista.zip"'
        return response