## Cloud Computing - Load Balancer
This project implements a load balancer for a cloud computing environment. The load balancer distributes incoming network traffic across multiple backend servers to ensure no single server becomes overwhelmed. This enhances the overall performance and reliability of the cloud service.

Project Overview
The load balancer manages traffic distribution to backend virtual machines (VMs) and ensures efficient handling of client requests. The key components of this project include:

Backend VM Script (backend-vm.py): This script manages the backend virtual machines that handle the actual client requests. Each VM operates independently, providing the necessary computational resources.

Host Script (host.py): This script is responsible for managing the host environment where the VMs are deployed. It oversees the lifecycle of the VMs, including their creation, monitoring, and deletion.

Load Balancer Script (load-ball.py): This is the core script for the load balancer. It monitors incoming client requests and distributes them across the available backend VMs based on a chosen load-balancing algorithm.
