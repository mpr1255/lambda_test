Some tricky issues to resolve: 

# getting tesseract to work in lambda;

Info on that here: https://github.com/shelfio/aws-lambda-tesseract

and more online

# getting exiftool to work in lambda
 
Here is the package: https://pypi.org/project/PyExifTool/ 

note it has to be built into the lambda environment, see more info here: https://aws.amazon.com/blogs/compute/running-executables-in-aws-lambda/ and https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html.

 So you may have to dig into the exiftool docs to figure that out: 

 There are also some binaries: https://github.com/pulsejet/exiftool-bin

 the github for the project is here: https://github.com/exiftool/exiftool

# getting Tika to work in lambda

This info may be helpful: 
https://github.com/shelfio/java-lambda-layer

With that all sorted out, this should work. 