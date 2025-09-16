class ContextManager:
    def __init__(self):
        self.history = []
        self.containers = {}

    def add_user_input(self, question: str):
        self.history.append({"role": "user", "content": question})
    def add_assistant_response(self, response: str):
        self.history.append({"role": "assistant", "content": response})

    def get_context(self):
        context = "\n".join([f"{item['role']}: {item['content']}" for item in self.history])
        if self.containers:
            context += "\n\nContainer Statuses:\n"
            for container_name, status in self.containers.items():
                context += f"- {container_name}: {status}\n"
        return context

    def update_container_status(self, container_name: str, status: str):
        self.containers[container_name] = status
    
    def remove_container(self, container_name: str):
        if container_name in self.containers:
            del self.containers[container_name]

    def get_container_status(self, container_name: str):
        return self.containers[container_name]
