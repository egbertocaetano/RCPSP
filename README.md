# RCPSP
Resource Constrained Project Scheduling Problem

O RCPSP trata problemas de escalonamento de atividades pertencentes há um projeto, onde deve ser considerado a precedência das atividades e a disponibilidade dos recursos limitados. 
O objetivo do RCPSP é minimizar o tempo dedicado para a execução de todas atividades de um determinado projeto.
O RCPSP é classificado como problema NP-Difícil.

Formulação do RCPSP
O RCPSP contém n+2 atividades J={0,1,2,...n+1} onde j=0 e j=n+1 são atividades fictícias que representam início e fim respectivamente.
Existem K tipos de recursos variados K={1,2,...K}. Enquanto o processo, uma atividade j requer rj,k unidades do recurso tipo k ϵ K durante cada período de sua duração t não preemptiva.
O recurso tipo k tem uma capacidade limite Rk em qualquer ponto do tempo.

Restrições do RCPSP:
  - Cada atividade só pode ser executada após todas as suas atividades precedentes tenham terminado sua execução.
  - A disponibilidade e limite dos recursos devem ser respeitado.
