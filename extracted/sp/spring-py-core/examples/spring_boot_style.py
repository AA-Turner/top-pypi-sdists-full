"""
Spring Boot风格的应用示例
"""
from spring_py import Component, Autowired, SpringBootApplication, get_bean, Bean, Configuration

@Component
class EmailService:
    def send_email(self, to, subject):
        print(f"📧 Sending email to {to}: {subject}")
        return f"Email sent to {to}"

@Component
class UserService:
    # 使用类型注解和Autowired装饰器进行依赖注入
    email_service: EmailService = Autowired()
    
    def __init__(self):
        self.users = {}
        print("📋 UserService created")
    
    def create_user(self, username, email):
        user_id = len(self.users) + 1
        self.users[user_id] = {'username': username, 'email': email}
        
        # 依赖注入的服务会自动可用
        if self.email_service:
            self.email_service.send_email(email, f"Welcome {username}!")
        
        print(f"👤 User created: {username} (ID: {user_id})")
        return user_id
    
    def get_user(self, user_id):
        return self.users.get(user_id)

@Component
class OrderService:
    user_service: UserService = Autowired()
    
    def __init__(self):
        self.orders = {}
        print("🛒 OrderService created")
    
    def create_order(self, user_id, amount):
        user = self.user_service.get_user(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        order_id = len(self.orders) + 1
        self.orders[order_id] = {
            'user_id': user_id,
            'amount': amount,
            'status': 'pending'
        }
        
        print(f"🛍️  Order created: ${amount} for {user['username']} (Order ID: {order_id})")
        return order_id

class BeanService:
    def __init__(self, num):
        self.num = num

    def print(self):
        print(self.num)

@Configuration
class ServiceConfig:
    def __init__(self):
        print("⚙️ ServiceConfig initialized")

    @Bean
    def injectService(self):
        return BeanService(42)

@SpringBootApplication()
class Application:
    """Spring Boot应用主类"""
    pass

def main():
    print("=== Spring Boot风格应用 ===")
    
    # 启动应用（类似Spring Boot）
    app = Application()
    context = app.run()
    
    print(f"\n🔧 Available components: {[c.__name__ for c in context.list_components()]}")
    
    # 获取服务并测试依赖注入
    print("\n📝 Testing dependency injection...")

    user_service: UserService = get_bean(UserService)
    order_service: OrderService = get_bean(OrderService)

    # 创建用户
    user_id = user_service.create_user("alice", "alice@example.com")
    
    # 创建订单（会自动使用注入的UserService）
    order_id = order_service.create_order(user_id, 99.99)
    
    print(f"\n✅ Application running successfully!")
    print(f"   User: {user_service.get_user(user_id)}")
    print(f"   Order: {order_service.orders.get(order_id)}")
    
    # 测试@Bean注入
    print(f"\n📦 Testing @Bean injection...")
    bean_service = get_bean(BeanService)
    if bean_service:
        print(f"   ✓ Got BeanService: {bean_service}")
        bean_service.print()
    else:
        print(f"   ❌ Failed to get BeanService")
    
    # 也可以按名称获取
    bean_by_name = get_bean("injectservice")
    if bean_by_name:
        print(f"   ✓ Got BeanService by name: {bean_by_name}")
    else:
        print(f"   ❌ Failed to get BeanService by name")

if __name__ == "__main__":
    main()
