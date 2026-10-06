# infrastructure/pdf/generator.py
import urllib.request
from io import BytesIO
from typing import List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from domain.interfaces import PDFGeneratorInterface
from domain.models import EnrollmentCertificateData


class ReportLabPDFGenerator(PDFGeneratorInterface):
    """
    Implementação concreta da interface PDFGeneratorInterface utilizando a biblioteca ReportLab.
    """

    def _download_image(self, url: Optional[str]) -> Optional[BytesIO]:
        """Método auxiliar para carregar a imagem da assinatura via URL em memória."""
        if not url:
            return None
        try:

            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return BytesIO(response.read())
        except Exception:
            # Em caso de falha na busca da imagem, continua sem interromper a geração
            return None

    def generate_students_list_pdf(
        self, enrollments: List[EnrollmentCertificateData]
    ) -> BytesIO:
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        page_width, page_height = A4

        # Cabeçalho do Relatório
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, page_height - 50, "LISTA CONSOLIDADA DE ALUNOS E CURSOS")

        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(colors.HexColor("#555555"))
        pdf.drawString(
            50,
            page_height - 68,
            f"Total de registros: {len(enrollments)} | Identificador do Tenant: {enrollments[0].tenant_id}",
        )

        # Linha Divisória
        pdf.setStrokeColor(colors.HexColor("#CCCCCC"))
        pdf.line(50, page_height - 80, page_width - 50, page_height - 80)

        # Tabela Simples
        y_position = page_height - 110
        pdf.setFillColor(colors.black)

        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(50, y_position, "#")
        pdf.drawString(80, y_position, "Aluno / Documento")
        pdf.drawString(280, y_position, "Curso")
        pdf.drawString(450, y_position, "Instrutor")

        y_position -= 20
        pdf.setFont("Helvetica", 10)

        for idx, item in enumerate(enrollments, start=1):
            if y_position < 50:  # Paginação
                pdf.showPage()
                y_position = page_height - 50
                pdf.setFont("Helvetica", 10)

            pdf.drawString(50, y_position, str(idx))
            pdf.drawString(
                80,
                y_position,
                f"{item.student.name} ({item.student.document})",
            )
            pdf.drawString(280, y_position, item.course.name)
            pdf.drawString(450, y_position, item.instructor.name)

            y_position -= 25

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return buffer

    def generate_individual_certificate_pdf(
        self, enrollment: EnrollmentCertificateData
    ) -> BytesIO:
        buffer = BytesIO()
        # Formato Paisagem (A4 Deitado) ideal para certificados
        pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
        page_width, page_height = landscape(A4)

        # Moldura Decorativa Externa
        pdf.setStrokeColor(colors.HexColor("#1A365D"))
        pdf.setLineWidth(4)
        pdf.rect(20, 20, page_width - 40, page_height - 40)

        # Moldura Interna Fina
        pdf.setLineWidth(1)
        pdf.rect(25, 25, page_width - 50, page_height - 50)

        # Título Principal
        pdf.setFont("Helvetica-Bold", 28)
        pdf.setFillColor(colors.HexColor("#1A365D"))
        pdf.drawCentredString(page_width / 2, page_height - 100, "CERTIFICADO DE CONCLUSÃO")

        # Texto de Certificação
        pdf.setFont("Helvetica", 14)
        pdf.setFillColor(colors.HexColor("#333333"))
        pdf.drawCentredString(
            page_width / 2,
            page_height - 150,
            "Certificamos para os devidos fins que",
        )

        # Nome do Aluno
        pdf.setFont("Helvetica-Bold", 22)
        pdf.setFillColor(colors.HexColor("#0D9488"))
        pdf.drawCentredString(page_width / 2, page_height - 190, enrollment.student.name)

        # Documento do Aluno e Descrição do Curso
        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(colors.black)
        pdf.drawCentredString(
            page_width / 2,
            page_height - 220,
            f"portador(a) do documento nº {enrollment.student.document}, concluiu com êxito o curso de",
        )

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(page_width / 2, page_height - 250, enrollment.course.name)

        pdf.setFont("Helvetica", 12)
        pdf.drawCentredString(
            page_width / 2,
            page_height - 280,
            f"com carga horária de {enrollment.course.duration_hours} horas, realizado no período de "
            f"{enrollment.course.start_date.strftime('%d/%m/%Y')} a {enrollment.course.end_date.strftime('%d/%m/%Y')}.",
        )

        # Seção de Assinaturas (Rodapé)
        y_sig = 110

        # Assinatura do Aluno
        pdf.line(120, y_sig, 350, y_sig)
        student_sig_img = self._download_image(enrollment.student.signature_url)
        if student_sig_img:
            try:

                pdf.drawImage(
                    student_sig_img,
                    180,
                    y_sig + 5,
                    width=100,
                    height=40,
                    mask='auto',
                    preserveAspectRatio=True,
                )
            except Exception:
                pass
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(235, y_sig - 15, enrollment.student.name)
        pdf.setFont("Helvetica", 9)
        pdf.drawCentredString(235, y_sig - 28, f"Aluno(a) - Doc: {enrollment.student.document}")

        # Assinatura do Instrutor
        pdf.line(page_width - 350, y_sig, page_width - 120, y_sig)
        instructor_sig_img = self._download_image(enrollment.instructor.signature_url)
        if instructor_sig_img:
            try:

                pdf.drawImage(
                    instructor_sig_img,
                    page_width - 290,
                    y_sig + 5,
                    width=100,
                    height=40,
                    mask='auto',
                    preserveAspectRatio=True,
                )
            except Exception:
                pass
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(page_width - 235, y_sig - 15, enrollment.instructor.name)
        pdf.setFont("Helvetica", 9)
        pdf.drawCentredString(
            page_width - 235, y_sig - 28, f"Instrutor(a) - Doc: {enrollment.instructor.document}"
        )

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return buffer