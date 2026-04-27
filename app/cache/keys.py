class CacheKey:
    @staticmethod
    def user_tasks(user_id: str) -> str:
        """all tasks for a user"""
        return f"tasks:user:{user_id}"
    
    @staticmethod
    def single_task(task_id: str) -> str:
        """single task by taskid"""
        return f"tasks:single:{task_id}"
    
    @staticmethod
    def user_profile(user_id: str) -> str:
        """user's profile data"""
        return f"user:profile:{user_id}"
        