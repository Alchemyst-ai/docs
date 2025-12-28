"""
Simple CLI QnA Agent with Alchemyst AI Memory
Uses OpenAI for chat completion and Alchemyst AI for persistent memory
"""

import os
import time
from datetime import datetime
from typing import Dict, List

from alchemyst_ai import AlchemystAI
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class QnAAgent:
    """A simple CLI-based Question & Answer agent with memory"""

    def __init__(self):
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize Alchemyst AI client for memory
        self.alchemyst_client = AlchemystAI(api_key=os.getenv("ALCHEMYST_AI_API_KEY"))

        # Session configuration
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.context_group = "qna_agent"
        self.conversation_history: List[Dict[str, str]] = []

        print(f"✓ QnA Agent initialized (Session: {self.session_id})")

    def save_to_memory(self, role: str, content: str):
        """Save conversation turn to Alchemyst memory"""
        try:
            memory_entry = {
                "timestamp": datetime.now().isoformat(),
                "session_id": self.session_id,
                "role": role,
                "content": content,
            }

            self.alchemyst_client.v1.context.add(
                documents=[
                    {
                        "content": f"{role}: {content}",
                        "metadata": {
                            "filename": f"{self.session_id}_{len(self.conversation_history)}",
                            "filetype": "txt",
                            "groupName": [self.context_group, self.session_id],
                        },
                    }
                ],
                source="conversation",
                context_type="conversation",
                scope="internal",
                metadata={
                    "file_name": f"{self.session_id}_{len(self.conversation_history)}",
                    "file_size": len(content),
                    "file_type": "ai/conversation",
                    "group_name": ["test_group"],
                    "last_modified": datetime.now().isoformat(),
                },
            )
        except Exception as e:
            print(f"Warning: Failed to save to memory: {e}")

    def get_relevant_context(self, query: str, limit: int = 3) -> str:
        """Retrieve relevant context from Alchemyst memory"""
        try:
            results = self.alchemyst_client.v1.context.search(
                query=query,
                similarity_threshold=0.6,
                minimum_similarity_threshold=0.2,
                scope="internal",
                body_metadata=None,  # {"groupName": [self.context_group]},
            )

            print("🔍 Retrieving relevant context from memory...")
            print(results.contexts)
            if results.contexts:
                context_items = []
                for i, result in enumerate(results.contexts[:limit]):
                    content = getattr(result, "content", "")
                    context_items.append(f"{i + 1}. {content}")

                return "\n".join(context_items)
            return ""
        except Exception as e:
            print(f"Warning: Failed to retrieve context: {e}")
            return ""

    def ask(self, question: str) -> str:
        """Ask a question and get an answer with memory context"""

        # Get relevant context from memory
        relevant_context = self.get_relevant_context(question)

        # Build system message with context
        system_message = "You are a helpful AI assistant with memory. "
        if relevant_context:
            system_message += (
                f"\n\nRelevant context from previous conversations:\n{relevant_context}"
            )

        # Add current question to conversation history
        self.conversation_history.append({"role": "user", "content": question})

        # Prepare messages for OpenAI (last 10 messages to stay within token limits)
        messages = [
            {"role": "system", "content": system_message}
        ] + self.conversation_history[-10:]

        # Get response from OpenAI
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini", messages=messages, temperature=0.7, max_tokens=500
            )

            answer = response.choices[0].message.content

            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": answer})

            # Save both question and answer to Alchemyst memory
            self.save_to_memory("user", question)
            self.save_to_memory("assistant", answer)

            return answer

        except Exception as e:
            return f"Error: {e}"

    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print("\nNo conversation history yet.")
            return

        print("\n" + "=" * 60)
        print("CONVERSATION HISTORY")
        print("=" * 60)

        for i, msg in enumerate(self.conversation_history, 1):
            role = "You" if msg["role"] == "user" else "Agent"
            print(f"\n[{i}] {role}: {msg['content']}")

        print("\n" + "=" * 60)

    def search_memory(self, query: str):
        """Search through all saved memories"""
        try:
            results = self.alchemyst_client.v1.context.search(
                query=query,
                similarity_threshold=0.5,
                scope="internal",
                minimum_similarity_threshold=0.2,
                body_metadata=None,  # {"groupName": [self.context_group]},
            )

            print("🔍 Searching memory...")
            print(results.contexts)

            if results.contexts:
                print(f"\n🔍 Found {len(results.contexts)} relevant memories:")
                print("=" * 60)
                for i, result in enumerate(results.contexts[:5], 1):
                    content = getattr(result, "content", "")
                    print(f"\n[{i}] {content}")
                print("\n" + "=" * 60)
            else:
                print("\n🔍 No relevant memories found.")
        except Exception as e:
            print(f"Error searching memory: {e}")


def print_welcome():
    """Print welcome message"""
    print("\n" + "=" * 60)
    print("       CLI QnA AGENT WITH MEMORY")
    print("       Powered by OpenAI + Alchemyst AI")
    print("=" * 60)
    print("\nCommands:")
    print("  - Type your question to get an answer")
    print("  - 'history' - Show conversation history")
    print("  - 'search <query>' - Search through saved memories")
    print("  - 'exit' or 'quit' - Exit the program")
    print("\n" + "=" * 60 + "\n")


def main():
    """Main CLI loop"""

    # Print welcome message
    print_welcome()

    # Initialize agent
    try:
        agent = QnAAgent()
    except Exception as e:
        print(f"\n❌ Failed to initialize agent: {e}")
        print("\nPlease ensure you have set the following environment variables:")
        print("  - OPENAI_API_KEY")
        print("  - ALCHEMYST_AI_API_KEY")
        return

    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle exit commands
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\n👋 Goodbye! Your conversation has been saved to memory.")
                break

            # Handle history command
            if user_input.lower() == "history":
                agent.show_history()
                continue

            # Handle search command
            if user_input.lower().startswith("search "):
                query = user_input[7:].strip()
                if query:
                    agent.search_memory(query)
                else:
                    print("\n⚠️  Please provide a search query: search <query>")
                continue

            # Process question
            print("\n🤖 Agent: ", end="", flush=True)
            answer = agent.ask(user_input)
            print(answer)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Your conversation has been saved to memory.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main2():
    """Add Google data to Alchemyst AI and search for 'founders of Google', measuring latency."""

    try:
        alchemyst_client = AlchemystAI(api_key=os.getenv("ALCHEMYST_AI_API_KEY"))
    except Exception as e:
        print(f"Failed to initialize AlchemystAI: {e}")
        return

    # Data to add
    google_info = (
        "Google LLC is an American multinational technology company. "
        "It was founded in September 1998 by Larry Page and Sergey Brin while they were PhD students at Stanford University."
    )

    # Add data
    try:
        start_add = time.time()
        alchemyst_client.v1.context.add(
            documents=[
                {
                    "content": google_info,
                    "metadata": {
                        "filename": "memory_google_info",
                        "filetype": "text/plain",
                        "groupName": ["test_group"],
                    },
                }
            ],
            source="manual_entry",
            context_type="resource",
            scope="internal",
            metadata={
                "file_name": "memory_google_info",
                "file_size": len(google_info),
                "file_type": "ai/conversation",
                "group_name": ["test_group"],
                "last_modified": datetime.now().isoformat(),
            },
        )
        end_add = time.time()
        print(
            f"Added Google info to Alchemyst AI (latency: {end_add - start_add:.3f}s)"
        )
    except Exception as e:
        print(f"Failed to add data: {e}")
        return

    # Search for "founders of Google"
    try:
        start_search = time.time()
        results = alchemyst_client.v1.context.search(
            query="founders of Google",
            similarity_threshold=0.5,
            minimum_similarity_threshold=0.2,
            scope="internal",
            body_metadata=None,
        )
        end_search = time.time()
        print(
            f"Searched for 'founders of Google' (latency: {end_search - start_search:.3f}s)"
        )
        if results.contexts:
            print("Search results:")
            for i, result in enumerate(results.contexts, 1):
                content = getattr(result, "content", "")
                print(f"[{i}] {content}")
        else:
            print("No relevant results found.")
    except Exception as e:
        print(f"Failed to search: {e}")


if __name__ == "__main__":
    main2()
