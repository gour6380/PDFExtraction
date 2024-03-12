import Vapor
import PythonKit

struct UploadFormData: Content {
    var file: File
    var password: String?
}

func routes(_ app: Application) throws {
    // Function to read file data
    func readFileData(path: String) -> Data? {
        try? Data(contentsOf: URL(fileURLWithPath: path))
    }
    let subprocess = Python.import("subprocess")
    let os = Python.import("os")
    let sys = Python.import("sys")

    os.chdir("pdf_lib");

    // Get the current working directory directly, as it's not an Optional
    let cwd = os.getcwd()


    let install_lib = subprocess.run(["pip3", "install", "."])

    //Check if the command was successful
    if install_lib.returncode == 0 {
        print("Package installed successfully.")
    }
    else{
        print("Failed to install package.")
    }

    sys.path.append(cwd) // Add the path to your custom package
    let myPDFlib = Python.import("pdf_lib")

    app.get { req -> EventLoopFuture<View> in
        return req.view.render("upload.html")
    }

    app.post("upload") { req -> EventLoopFuture<String> in
    
        let uploadedFile = try req.content.decode(UploadFormData.self)

        let fileData = Data(buffer: uploadedFile.file.data)

        let byteArray = [UInt8](fileData)

        let pythonData = Python.bytes(byteArray)

        // Access the password (if provided)
        if let password = uploadedFile.password {

            let result = myPDFlib.main(pythonData, password)
            let extractedText = String(describing: result)
            return req.eventLoop.future(extractedText)

        } else {
            let result = myPDFlib.main(pythonData)
            let extractedText = String(describing: result)
            return req.eventLoop.future(extractedText)

        }
    }
}
