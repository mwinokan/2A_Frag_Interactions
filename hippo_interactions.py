#!/usr/bin/env python

import hippo
import mrich
from mrich import print
from typer import Typer

app = Typer()


@app.command()
def main(prolif: bool = False):

    if prolif:
        animal = hippo.HIPPO("2A_Frag_Interactions", "2a_interactions_prolif.sqlite")

    else:
        animal = hippo.HIPPO("2A_Frag_Interactions", "2a_interactions.sqlite")

    animal.add_hits(
        "A71EV2A", "A71EV2A_frags/metadata.csv", "A71EV2A_frags/aligned_files"
    )

    for pose in mrich.track(animal.poses):
        if prolif:
            pose.calculate_prolif_interactions()
        else:
            pose.calculate_interactions()

    mrich.var("#poses", animal.num_poses)
    mrich.var("#profiled", animal.poses.num_fingerprinted)

    df = animal.interactions.df

    # add pose names
    name_lookup = animal.poses.id_name_dict
    df["pose_name"] = df["pose_id"].map(name_lookup)

    # add pose longnames
    longname_lookup = {p.id: p.metadata["observation_longname"] for p in animal.poses}
    df["pose_longname"] = df["pose_id"].map(longname_lookup)

    df.set_index("pose_longname", inplace=True)

    if prolif:
        mrich.writing("2A_fragment_interactions_prolif.csv")
        df.to_csv("2A_fragment_interactions_prolif.csv")

    else:
        mrich.writing("2A_fragment_interactions.csv")
        df.to_csv("2A_fragment_interactions.csv")


if __name__ == "__main__":
    app()
