import redis

class TaskManager:
    def __init__(self, host='172.27.8.177', port=6379, db=0, username='evolv', password='aeac70a405c5bbfe5b1b9b083fcdcb6a3db8899dd12af52412cba21fd2e57941'):
        """Initialize the Task Manager with a connection to Redis Stack with authentication"""
        # Connect to Redis Stack with authentication (username/password)
        self.redis_client = redis.StrictRedis(
            host=host, 
            port=port, 
            db=db, 
            username=username,  # Redis username for ACL
            password=password,  # Redis password for authentication
            decode_responses=True
        )

    def add_task(self, task_id, task_title):
        """Add a new task to Redis Stack with status 'pending'."""
        task = {'title': task_title, 'status': 'pending'}
        self.redis_client.hmset(f'task:{task_id}', task)
        print(f"Task '{task_title}' added with ID {task_id}")

    def view_tasks(self):
        """View all tasks."""
        task_keys = self.redis_client.keys('task:*')  # Get all task keys
        if not task_keys:
            print("No tasks available.")
            return
        
        for key in task_keys:
            task = self.redis_client.hgetall(key)
            print(f"Task ID: {key.decode('utf-8').split(':')[1]} - Title: {task['title']} - Status: {task['status']}")

    def mark_task_completed(self, task_id):
        """Mark a task as completed."""
        task_key = f'task:{task_id}'
        if not self.redis_client.exists(task_key):
            print(f"Task with ID {task_id} does not exist.")
            return
        
        self.redis_client.hset(task_key, 'status', 'completed')
        print(f"Task {task_id} marked as completed.")

    def view_tasks_by_status(self, status):
        """View tasks by status."""
        task_keys = self.redis_client.keys(f'task:*')
        if not task_keys:
            print(f"No tasks with status '{status}' available.")
            return

        for key in task_keys:
            task = self.redis_client.hgetall(key)
            if task['status'] == status:
                print(f"Task ID: {key.decode('utf-8').split(':')[1]} - Title: {task['title']} - Status: {task['status']}")


if __name__ == '__main__':
    # Replace with your Redis Stack server details and credentials
    redis_host = '172.27.8.177'  # Redis server IP address (e.g., 192.168.1.100)
    redis_port = 6379  # Default Redis port
    redis_username = 'evolv'  # The username for Redis (ACL-based authentication)
    redis_password = 'aeac70a405c5bbfe5b1b9b083fcdcb6a3db8899dd12af52412cba21fd2e57941'  # The password for Redis
    
    task_manager = TaskManager(
        host=redis_host,
        port=redis_port,
        username=redis_username,
        password=redis_password
    )

    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Completed")
        print("4. View Tasks by Status")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            task_id = input("Enter task ID: ")
            task_title = input("Enter task title: ")
            task_manager.add_task(task_id, task_title)
        
        elif choice == '2':
            task_manager.view_tasks()
        
        elif choice == '3':
            task_id = input("Enter task ID to mark as completed: ")
            task_manager.mark_task_completed(task_id)
        
        elif choice == '4':
            status = input("Enter status (pending/completed): ")
            task_manager.view_tasks_by_status(status)
        
        elif choice == '5':
            print("Exiting the Task Manager.")
            break
        
        else:
            print("Invalid choice. Please try again.")
