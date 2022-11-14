const generatorPDF = async (name) => {
    const {PDFDocument, rgb} = PDFLib;
    const exBytes = await fetch("/static/assets/cert.pdf").then((res) => {
        
        return res.arrayBuffer();
    });
    const exFont = await fetch("/static/assets/fonts/Sanchez-Regular.ttf").then((res) => {
        return res.arrayBuffer();
    })

    console.log(name.length)

    const pdfDoc = await PDFDocument.load(exBytes)
    pdfDoc.registerFontkit(fontkit);

    const myFont = await pdfDoc.embedFont(exFont);

    const pages = pdfDoc.getPages();
    const firstPg = pages[0];
    
    var x = name.length * 5.5

    if (name.length > 19){
        console.log('betol')
        firstPg.drawText(name, {
            x:120 - x,
            y:220
        })
    }
    else{
        firstPg.drawText(name, {
            x:120 - x,
            y:220
        })
    }

    const uri = await pdfDoc.saveAsBase64({dataUri:true})
    

    d = $("#mypdf").attr('src', uri)
     
}

generatorPDF("KUSUMA");