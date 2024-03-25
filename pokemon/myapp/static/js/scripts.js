function downloadPDF() {
    var options = {
        margin: 20,
        filename: 'formulario.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { 
            unit: 'mm', 
            format: 'a4', 
            orientation: 'portrait',
            pagebreak: { mode: 'avoid-all' } 
        }
    };

    var element = document.querySelector('.content-container');

    html2pdf()
        .set(options)
        .from(element)
        .save();
}

document.getElementById('download-btn').addEventListener('click', downloadPDF);