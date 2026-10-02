#import <Foundation/Foundation.h>
#import <ReactCommon/RCTTurboModule.h>

NS_ASSUME_NONNULL_BEGIN

// Vends the pure C++ `DiscordMarkdown` TurboModule. Wired up by codegen through
// `codegenConfig.ios.modulesProvider` in package.json.
@interface DiscordMarkdownModuleProvider : NSObject <RCTModuleProvider>

@end

NS_ASSUME_NONNULL_END
