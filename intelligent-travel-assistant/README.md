Intelligent-travel-assistant
- Build an intelligent travel assistant that can handle step-by-step tasks. 
- The agent must demonstrate clear logical planning capabilities. It needs to first call the weather query tool and use the obtained observation results as the basis for the next step. In the next round of the loop, it then calls the attraction recommendation tool to arrive at the final suggestion.
- Tools we use:
  1. tavily-python is a powerful AI search API client for obtaining real-time web search results.
  2. weather query service wttr.in, which can return weather data for a specified city in JSON format.
