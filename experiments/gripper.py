#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from basilisk import BENCHMARK_DIR
from basilisk.incremental import IncrementalExperiment

from defaults import generate_experiment


def experiment(experiment_name):
    domain = "domain.pddl"
    domain_dir = "gripper-m"
    benchmark_dir = BENCHMARK_DIR

    experiments = dict()

    # Experiment used in the paper
    experiments["gripper_std_inc"] = dict(
        lp_max_weight=5,
        experiment_class=IncrementalExperiment,
        instances=['test01.pddl',
                   'test02.pddl',
                   'test03.pddl',
                   'test04.pddl',
                   'test05.pddl',
                   'test06.pddl',
                   'prob03.pddl',
                   'prob_3balls_3rooms_1rob.pddl'],
        test_instances=["prob01.pddl",
                        "prob02.pddl",
                        "prob03.pddl",
                        "prob04.pddl",
                        "prob05.pddl",
                        "prob06.pddl",
                        'prob_3balls_3rooms_1rob.pddl',
                        "prob_4balls_4rooms_1rob.pddl",
                        "prob_4balls_4rooms_2rob.pddl",
                        "prob_10balls_4rooms_1rob.pddl",],
        test_domain=domain,
        # This is number of sampled states *per training instance*. In an increm. experiment, they will be processed
        # in batches, so we can set them high enough.
        num_states=12000,
        initial_sample_size=100,
        max_concept_grammar_iterations=None, random_seed=19,
        initial_concept_bound=8, max_concept_bound=12, concept_bound_step=2,
        batch_refinement_size=50,
        clean_workspace=False,
        parameter_generator=None,  # add_domain_parameters,
        feature_namer=feature_namer,
    )

    # Select the actual experiment parameters according to the command-line option
    parameters = experiments[experiment_name]
    parameters["domain_dir"] = parameters.get("domain_dir", domain_dir)
    parameters["domain"] = parameters.get("domain", domain)
    return generate_experiment(**parameters)


def add_domain_parameters(language):
    return [language.constant("roomb", "object")]


def feature_namer(feature):
    s = str(feature)
    return {
        "card[free]": "nfree-grippers",
        "bool[Exists(at-robby,{roomb})]": "robby-is-at-B",
        "card[Exists(at,Exists(Inverse(at-robby),<universe>))]": "nballs-in-room-with-some-robot",
        "card[And(Exists(gripper,Exists(at-robby,{roomb})),free)]": "nfree-grippers-at-B",
        "card[Exists(at,{roomb})]": "nballs-at-B",
        "card[Exists(at,Not({roomb}))]": "nballs-not-at-B",
        "card[Exists(carry,<universe>)]": "nballs-carried",
        "card[Exists(at-robby,{roomb})]": "nrobots-at-B",
        "card[Exists(gripper,Exists(at-robby,{roomb}))]": "ngrippers-at-B",
        "card[Exists(carry,Exists(gripper,Exists(at-robby,{roomb})))]": "nballs-carried-in-B",
        "card[Exists(at,And(Forall(Inverse(at-robby),<empty>), Not({roomb})))]": "nballs-in-some-room-notB-without-any-robot",
        "card[Forall(at,And(Forall(Inverse(at-robby),<empty>),Not({roomb})))]": "nballs-either-held-or-in-a-room-!=B-with-no-robot",
        "card[Forall(at,{roomb})]": "nballs-being-carried-or-in-B",
        "card[Forall(carry,Exists(gripper,Exists(at-robby,{roomb})))]": "nballs-either-not-carried-or-in-room-B"
        # "": "",
    }.get(s, s)


if __name__ == "__main__":
    exp = experiment(sys.argv[1])
    exp.run(sys.argv[2:])
