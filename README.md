# Pod Patrol - AI-Powered Kubernetes Debugger

Pod Patrol is an intelligent Kubernetes debugging tool that leverages Large Language Models (LLMs) to diagnose cluster issues and suggest fixes. 
This project demonstrates multi-agent test-time compute for improved reliability, combining DevOps automation with AI to provide an interactive CLI interface for Kubernetes troubleshooting.

## Overview

Kubernetes deployments can become complex and difficult to debug due to their distributed, stateless nature. Pod Patrol solves this by:
- **Multi-Agent Test-Time Compute**: Uses multiple AI agents to validate solutions and improve accuracy
- **Conversational Interface**: Natural language interaction for cluster diagnosis
- **Automated Cluster Analysis**: Real-time kubectl command execution and parsing
- **Solution Validation**: Optional multi-agent consensus for critical recommendations

## Features

### Core Functionality
- **Interactive CLI Interface**: Chat-based interaction for natural troubleshooting
- **Automated Cluster Analysis**: Intelligent parsing of kubectl command outputs
- **Context Management**: Maintains conversation context for complex debugging sessions
- **Tool Integration**: Seamless kubectl integration for real-time cluster state queries

### Multi-Agent Test-Time Compute
- **Candidate Generation**: Primary agent generates multiple solution candidates
- **Cross-Validation**: Judge agents evaluate and rank proposed solutions
- **Consensus Building**: Multiple agents collaborate to improve answer quality
- **Error Reduction**: Test-time compute reduces hallucinations and improves reliability

## Quick Start

### Prerequisites

- Python 3.12+
- Docker and k3d for local Kubernetes testing
- kubectl configured for your cluster

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd pod-patrol
```

2. Set up the Python virtual environment:
```bash
python -m venv pod-patrol
source pod-patrol/bin/activate  # On Windows: pod-patrol\Scripts\activate
pip install -r requirements.txt
```

3. Configure your AI model API keys (see Configuration section)

### Basic Usage

Start the interactive debugger:
```bash
python pod_patrol.py
```

For multi-agent validation (test-time compute):
```bash
python pod_patrol.py --validate-solution --candidate-num 3
```

Example session:
```
> Why is my pod crashing?
Checking pod status...
[Analysis and recommendations follow]

> How can I fix the CrashLoopBackOff error?
Validating solution... (when using --validate-solution)
[Multiple agents collaborate on solution]
[Detailed troubleshooting steps with improved confidence]
```

## Testing Environment

The project includes a local k3d cluster setup for testing:

1. Follow instructions in `k3d-cluster/README.md` to set up the test cluster
2. Deploy test applications with intentional faults
3. Use Pod Patrol to diagnose and fix the issues

## Architecture

Pod Patrol uses a modular architecture designed for extensibility and reliability:

### Core Components

- **Agent Wrapper**: Handles LLM interactions and tool calling
- **Context Manager**: Maintains conversation state and cluster context
- **Judge Agent**: Validates solutions through multi-agent consensus
- **Tool Integration**: kubectl command execution and result parsing

### How It Works

1. **User Input**: Natural language questions about cluster issues
2. **Context Analysis**: Builds understanding of current cluster state
3. **Tool Execution**: Runs kubectl commands to gather diagnostic information
4. **AI Analysis**: Primary LLM processes cluster data to identify issues
5. **Solution Generation**: Generates multiple candidate solutions
6. **Multi-Agent Validation**: Judge agents evaluate and rank solutions (when enabled)
7. **Consensus Output**: Delivers validated recommendations with improved confidence

### Kubernetes Integration

The tool integrates with Kubernetes through:
- kubectl command execution for real-time cluster state
- Manifest analysis for configuration issues  
- Pod logs and events examination
- Resource usage and health monitoring

## Advanced Features & Roadmap

### Implemented Features
- **Multi-agent test-time compute** for solution validation
- Context-aware conversation management  
- Comprehensive kubectl tool integration
- Interactive CLI with persistent sessions
- Candidate generation and consensus ranking

### Future Enhancements

**Documentation Integration**
- RAG-based Kubernetes documentation retrieval
- Vector database for intelligent doc search
- Context-aware documentation suggestions

**Evaluation & Testing**
- Automated diagnostic accuracy testing
- Benchmark suite for common K8s issues
- Performance metrics and success rate tracking

**Interface Improvements** 
- Web-based dashboard for cluster visualization
- REST API for integration with existing tools
- Mobile-friendly responsive interface

## Configuration

Set up your environment variables:
```bash
export OPENAI_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"  # Optional: for Claude models
```

## Contributing

This project welcomes contributions! Areas of interest:
- Additional kubectl tool integrations
- Enhanced diagnostic algorithms
- UI/UX improvements
- Documentation and examples

## License

MIT License - see LICENSE file for details.

## About

Built as a demonstration of multi-agent test-time compute applied to DevOps automation. This project explores how multiple AI agents can collaborate during inference to improve the reliability and accuracy of Kubernetes troubleshooting recommendations.
