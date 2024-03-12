import Vapor

// configures your application
public func configure(_ app: Application) async throws {
    // uncomment to serve files from /Public folder
    // app.middleware.use(FileMiddleware(publicDirectory: app.directory.publicDirectory))
    // Increase the maximum body size to, 10MB
    app.routes.defaultMaxBodySize = "10mb"
    // register routes
    try routes(app)
}
