from gym.envs.registration import registry, register, make, spec

# RDDL domains

for i in range(0, 100):
    register(
        id='RDDL-wildfire{}-v1'.format(i),
        entry_point='gym.envs.rddl:RDDLEnv',
        kwargs={
            'domain': 'wildfire',
            'instance': '{}'.format(i),
        })

# for i in range(1, 10100):
#     register(
#         id='RDDL-academic_advising{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'academic_advising',
#             'instance': '{}'.format(i),
#         })


#     register(
#         id='RDDL-corridor{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'corridor',
#             'instance': '{}'.format(i),
#         })
 
#     register(
#         id='RDDL-stochastic_wall{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'stochastic_wall',
#             'instance': '{}'.format(i),
#         })

#     register(
#         id='RDDL-stochastic_navigation{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'stochastic_navigation',
#             'instance': '{}'.format(i),
#         })

#     register(
#         id='RDDL-wall{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'wall',
#             'instance': '{}'.format(i),
#         })

#     register(
#         id='RDDL-academic_advising_prob{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'academic_advising_prob',
#             'instance': '{}'.format(i),
#         })

#     register(
#         id='RDDL-pizza_delivery_windy{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'pizza_delivery_windy',
#             'instance': '{}'.format(i),
#         })

#     register(
#         id='RDDL-pizza_delivery_grid{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'pizza_delivery_grid',
#             'instance': '{}'.format(i),
#         })

#     register(
#         id='RDDL-pizza_delivery{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'pizza_delivery',
#             'instance': '{}'.format(i),
#         })

    
#     register(
#         id='RDDL-academic_advising_chain{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'academic_advising_chain',
#             'instance': '{}'.format(i),
#         })

#     register(
#         id='RDDL-sysadmin{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'sysadmin',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-game_of_life{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'game_of_life',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-wildfire{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'wildfire',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-navigation{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'navigation',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-tamarisk{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'tamarisk',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-elevators{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'elevators',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-traffic{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'traffic',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-skill_teaching{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'skill_teaching',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-recon{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'recon',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-recon_new{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'recon_new',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-crossing_traffic{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'crossing_traffic',
#             'instance': '{}'.format(i)
#         })

#     register(
#         id='RDDL-triangle_tireworld{}-v1'.format(i),
#         entry_point='gym.envs.rddl:RDDLEnv',
#         kwargs={
#             'domain': 'triangle_tireworld',
#             'instance': '{}'.format(i)
#         })
